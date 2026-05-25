# Planner V5

V5 is the V4 planner rebuilt as a static Supabase app. The UI and behavior stay in `clientway2clean.html`; persistence now goes directly to Supabase instead of the Flask/SQLite backend.

## Setup

1. Create a Supabase project.
2. Open the Supabase SQL editor and run `supabase-schema.sql`.
3. Copy your project URL and anon public key from Supabase settings.
4. Put them in `supabase-config.js`.
5. Deploy the `V5` folder to Vercel as a static site.

The included schema uses public anon read/write policies because the current V4 app has no login system. That matches the existing behavior, but anyone with the deployed app can read and edit the planner data.
