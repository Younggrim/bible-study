// Deno entry point for the bible-audio Supabase Edge Function. All logic is
// in handler.ts. Deploy with JWT verification off: the site calls this with
// no Authorization header, and access is limited by origin instead.
//
//   supabase functions deploy bible-audio --no-verify-jwt --project-ref vqgumrfjxlhkzzzfgejl
import { handle } from "./handler.ts";

Deno.serve((req) => handle(req, { get: (k) => Deno.env.get(k) }));
