# DEPLOY.md — fielding SARA USA 2026 on Heroku

The plain-English runbook for putting the survey on the internet and collecting
real data. One-time setup takes ~30 minutes; after that, each DCE wave is a
four-step cycle you repeat.

## The concepts, translated

- **Heroku** — a company you rent a small server from. You send it this repo
  (`git push`), it runs the survey at `https://<your-app>.herokuapp.com`.
- **Postgres** — the database, rented as a Heroku add-on. It lives *separately*
  from the app, which matters here: we redeploy the app three times
  mid-fielding (once per DCE checkpoint), and responses from every wave must
  accumulate in one place that redeploys can't touch.
- **Config vars** (a.k.a. environment variables) — settings you type into
  Heroku once, like the admin password. They stay on the server and never go
  in git, which is why they're safe for secrets.
- **A room** — oTree's stable entry link (`/room/sara_usa`). The panel gets
  this one URL at the start and it keeps working all the way through fielding,
  even though behind the scenes you create a fresh session for each wave.

Files in this repo that exist for Heroku's benefit: `Procfile` (the command
Heroku runs to start the survey), `.python-version` (which Python to use —
pinned to 3.11, same as CI), and `psycopg2-binary` in `requirements.txt` (the
Postgres driver).

## One-time setup

1. **Install the Heroku CLI and log in** (free account at heroku.com first):

   ```sh
   brew tap heroku/brew && brew install heroku
   heroku login
   ```

2. **Create the app and the database** (from the repo root):

   ```sh
   heroku create sara-usa-2026        # pick any free name; it becomes the URL
   heroku addons:create heroku-postgresql:essential-0
   ```

3. **Set the secrets.** Generate two random strings and save both in your
   password manager — the admin password is how you'll log in; the secret key
   is what makes participant URLs unforgeable:

   ```sh
   python3 -c "import secrets; print('admin pw: ', secrets.token_urlsafe(16))"
   python3 -c "import secrets; print('secret key:', secrets.token_urlsafe(48))"

   heroku config:set \
     OTREE_PRODUCTION=1 \
     OTREE_AUTH_LEVEL=STUDY \
     OTREE_ADMIN_PASSWORD='<the admin pw>' \
     OTREE_SECRET_KEY='<the secret key>'
   ```

   `OTREE_AUTH_LEVEL=STUDY` locks the admin and demo pages behind that
   password. `DATABASE_URL` is set automatically by the Postgres add-on —
   don't set it yourself.

4. **Deploy and switch on:**

   ```sh
   git push heroku main
   heroku ps:scale web=1:basic       # Basic dyno: ~$7/mo, never sleeps
   ```

   (Deploying a branch instead of main: `git push heroku <branch>:main`.)

5. **Smoke-test.** Open `https://<your-app>.herokuapp.com` — you should be
   asked for the admin login (user `admin`, the password from step 3). In the
   admin, go to **Rooms → sara_usa**, create a session there with the config
   *SARA USA 2026* and enough participant slots for the wave. The room link

   ```
   https://<your-app>.herokuapp.com/room/sara_usa
   ```

   is what the panel gets. Walk through the whole survey yourself at that link
   before anyone else does — including the consent-decline path and the
   attention-check screen-out — then download the export (admin → **Data**)
   and eyeball the columns.

**Prolific specifics:** give Prolific the room URL with their participant ID
appended, so responses link to payments without you collecting names:

```
https://<your-app>.herokuapp.com/room/sara_usa?participant_label={{%PROLIFIC_PID%}}
```

and put Prolific's completion URL on the survey's final page so participants
get their completion code.

## Per-wave cycle (waves 2, 3, 4)

The sequential DCE re-optimises the choice tasks between waves
(PREREGISTRATION.md §5). When a wave finishes and the panel is paused:

1. **Export + back up.** Admin → **Data** → download the CSV export. Also:

   ```sh
   heroku pg:backups:capture && heroku pg:backups:download
   ```

2. **Run the checkpoint locally** (writes the new `survey/sara/dce_blocks.csv`
   plus the archived per-wave copy and the log):

   ```sh
   Rscript dce_sequential.R --checkpoint <2|3|4> <export1.csv> [...]
   ```

3. **Commit, tag, redeploy** (~2 min; earlier waves' data are safe in
   Postgres — this only replaces the app):

   ```sh
   git add -A && git commit -m "DCE checkpoint: wave <k> design"
   git tag wave-<k>
   git push heroku main --tags
   ```

   The tag is the audit trail: `wave-<k>` = exactly the instrument that was in
   the field for wave *k*.

4. **New session, same link.** In the admin, create a fresh session in the
   `sara_usa` room for the new wave, then tell the panel to resume. The room
   URL doesn't change.

During fielding, capture a Postgres backup (step 1's `pg:backups` command)
daily — it's one command and it's the difference between a bad day and a lost
study.

## Rules while data collection is live

- **Never change the instrument mid-wave.** Adding/removing items changes the
  database schema and oTree has no migration story — the design freeze in
  PREREGISTRATION.md and the wave-1 deploy are the same moment. Swapping
  `dce_blocks.csv` between waves is fine (same schema); editing
  `sara_usa.md` is not.
- **Never run `otree devserver` against production** — it's unauthenticated
  and resets the database on schema changes. Production runs `otree
  prodserver` via the `Procfile`; local piloting stays on your laptop's
  sqlite.
- If something looks wrong on the server: `heroku logs --tail`.

## Teardown (after wave 4 + final export)

```sh
heroku pg:backups:capture && heroku pg:backups:download   # final belt-and-braces
heroku ps:scale web=0        # stop the survey (keeps app + data, ~$5/mo for DB)
# ...and once the data are safely archived and analysed:
heroku apps:destroy sara-usa-2026
```

Running cost while fielding: ~$12/month (Basic dyno $7 + Essential-0 Postgres
$5). Destroy the app when done and the bill stops.
