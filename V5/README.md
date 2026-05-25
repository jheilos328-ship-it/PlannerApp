# Planner V5

V5 is the V4 planner rebuilt as a static Supabase app. The UI and behavior stay in `clientway2clean.html`; persistence now goes directly to Supabase instead of the Flask/SQLite backend.

## Setup

1. Create a Supabase project.
2. In Supabase Auth, enable the Email provider.
3. In Supabase Auth settings, disable public signups.
4. In Authentication > Users, create your personal user manually.
5. Open the Supabase SQL editor and run `supabase-schema.sql`.
6. Copy your project URL and anon public key from Supabase settings.
7. Put them in `supabase-config.js`.
8. Deploy the `V5` folder to Vercel as a static site.

The app has no public account creation flow. Only users you create in Supabase can sign in. The schema uses row-level security tied to `auth.uid()`, so projects are owned by the signed-in user, and subjects/notes are only accessible through projects owned by that same user.

If you already had public V5 data before adding auth, those existing projects will have a blank `user_id` and will be hidden by RLS until you assign them to your Supabase user id.
