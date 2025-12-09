-- tickets table
create table if not exists tickets (
  id bigserial primary key,
  title text,
  description text,
  requester_email text,
  status text default 'open',
  created_at timestamptz default now()
);

-- messages table
create table if not exists messages (
  id bigserial primary key,
  ticket_id bigint references tickets(id),
  role text, -- 'user', 'agent', 'system'
  content text,
  created_at timestamptz default now()
);

-- simple logs
create table if not exists logs (
  id bigserial primary key,
  level text,
  message text,
  created_at timestamptz default now()
);

