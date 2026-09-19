# BS605 progress sync — Supabase setup (5–10 min)

1. Open https://supabase.com/dashboard and sign in (GitHub is fine).
2. **New project** → any name (e.g. `amity-bs605`) → set a DB password → create.
3. Left sidebar **SQL Editor** → New query → paste all of [`supabase/setup.sql`](supabase/setup.sql) → **Run**.
4. **Project Settings → API**:
   - Copy **Project URL**
   - Copy **anon public** key
5. Paste them into [`config.js`](config.js):

```js
window.BS605_SYNC = {
  url: "https://xxxx.supabase.co",
  anonKey: "eyJhbGciOi..."
};
```

6. Commit + push (or tell the agent the two values) so GitHub Pages picks them up.

Then on the live site: enter one private sync code → **Connect**. Use the same code on phone and PC.
