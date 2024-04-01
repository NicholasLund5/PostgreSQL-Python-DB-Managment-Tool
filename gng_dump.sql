--
-- PostgreSQL database dump
--

-- Dumped from database version 10.23 (Ubuntu 10.23-0ubuntu0.18.04.2+esm1)
-- Dumped by pg_dump version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: campaignorganizers; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.campaignorganizers (
    employee integer NOT NULL,
    campaignid integer NOT NULL
);


ALTER TABLE public.campaignorganizers OWNER TO c370_s088;

--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.campaigns (
    campaignid integer NOT NULL,
    startdate date,
    enddate date,
    name character varying(255),
    description text,
    annotations text
);


ALTER TABLE public.campaigns OWNER TO c370_s088;

--
-- Name: campaigns_campaignid_seq; Type: SEQUENCE; Schema: public; Owner: c370_s088
--

CREATE SEQUENCE public.campaigns_campaignid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaigns_campaignid_seq OWNER TO c370_s088;

--
-- Name: campaigns_campaignid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: c370_s088
--

ALTER SEQUENCE public.campaigns_campaignid_seq OWNED BY public.campaigns.campaignid;


--
-- Name: events; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.events (
    eventid integer NOT NULL,
    type character varying(255),
    date date,
    location character varying(255),
    campaignid integer
);


ALTER TABLE public.events OWNER TO c370_s088;

--
-- Name: events_eventid_seq; Type: SEQUENCE; Schema: public; Owner: c370_s088
--

CREATE SEQUENCE public.events_eventid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_eventid_seq OWNER TO c370_s088;

--
-- Name: events_eventid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: c370_s088
--

ALTER SEQUENCE public.events_eventid_seq OWNED BY public.events.eventid;


--
-- Name: finances; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.finances (
    transactionid integer NOT NULL,
    type character varying(255),
    amount numeric(10,2),
    date date,
    campaignid integer,
    memberid integer
);


ALTER TABLE public.finances OWNER TO c370_s088;

--
-- Name: finances_transactionid_seq; Type: SEQUENCE; Schema: public; Owner: c370_s088
--

CREATE SEQUENCE public.finances_transactionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.finances_transactionid_seq OWNER TO c370_s088;

--
-- Name: finances_transactionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: c370_s088
--

ALTER SEQUENCE public.finances_transactionid_seq OWNED BY public.finances.transactionid;


--
-- Name: memberevents; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.memberevents (
    member integer NOT NULL,
    eventid integer NOT NULL
);


ALTER TABLE public.memberevents OWNER TO c370_s088;

--
-- Name: members; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.members (
    memberid integer NOT NULL,
    name character varying(255),
    role character varying(255),
    tier integer,
    numcampaigns integer,
    salary numeric(10,2),
    annotations text
);


ALTER TABLE public.members OWNER TO c370_s088;

--
-- Name: members_memberid_seq; Type: SEQUENCE; Schema: public; Owner: c370_s088
--

CREATE SEQUENCE public.members_memberid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.members_memberid_seq OWNER TO c370_s088;

--
-- Name: members_memberid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: c370_s088
--

ALTER SEQUENCE public.members_memberid_seq OWNED BY public.members.memberid;


--
-- Name: question1; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question1 AS
SELECT
    NULL::character varying(255) AS campaign_name,
    NULL::bigint AS num_events;


ALTER TABLE public.question1 OWNER TO c370_s088;

--
-- Name: question10; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question10 AS
 SELECT count(*) AS num_active_campaigns
   FROM public.campaigns
  WHERE ((CURRENT_DATE >= campaigns.startdate) AND (CURRENT_DATE <= campaigns.enddate));


ALTER TABLE public.question10 OWNER TO c370_s088;

--
-- Name: question2; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question2 AS
SELECT
    NULL::character varying(255) AS campaign_name,
    NULL::numeric AS total_expenses;


ALTER TABLE public.question2 OWNER TO c370_s088;

--
-- Name: question3; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question3 AS
SELECT
    NULL::character varying(255) AS member_name,
    NULL::bigint AS num_events_participated;


ALTER TABLE public.question3 OWNER TO c370_s088;

--
-- Name: website; Type: TABLE; Schema: public; Owner: c370_s088
--

CREATE TABLE public.website (
    updateid integer NOT NULL,
    content text,
    phase character varying(255),
    date date,
    publishedstatus boolean,
    campaignid integer
);


ALTER TABLE public.website OWNER TO c370_s088;

--
-- Name: question4; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question4 AS
 SELECT c.name AS campaign_name
   FROM public.campaigns c
  WHERE (NOT (EXISTS ( SELECT 1
           FROM public.website w
          WHERE ((c.campaignid = w.campaignid) AND (w.publishedstatus IS NOT NULL)))));


ALTER TABLE public.question4 OWNER TO c370_s088;

--
-- Name: question5; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question5 AS
SELECT
    NULL::character varying(255) AS campaign_name,
    NULL::numeric AS total_donations;


ALTER TABLE public.question5 OWNER TO c370_s088;

--
-- Name: question6; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question6 AS
 SELECT members.name
   FROM public.members
  WHERE (((members.role)::text = 'Volunteer'::text) AND (members.numcampaigns > 3));


ALTER TABLE public.question6 OWNER TO c370_s088;

--
-- Name: question7; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question7 AS
 SELECT e.type AS event_type,
    count(e.eventid) AS num_events
   FROM public.events e
  GROUP BY e.type;


ALTER TABLE public.question7 OWNER TO c370_s088;

--
-- Name: question8; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question8 AS
 SELECT events.eventid,
    events.type,
    events.date,
    events.location,
    events.campaignid
   FROM public.events
  WHERE (events.date < '2024-06-01'::date);


ALTER TABLE public.question8 OWNER TO c370_s088;

--
-- Name: question9; Type: VIEW; Schema: public; Owner: c370_s088
--

CREATE VIEW public.question9 AS
 SELECT avg(members.salary) AS average_salary
   FROM public.members;


ALTER TABLE public.question9 OWNER TO c370_s088;

--
-- Name: website_updateid_seq; Type: SEQUENCE; Schema: public; Owner: c370_s088
--

CREATE SEQUENCE public.website_updateid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_updateid_seq OWNER TO c370_s088;

--
-- Name: website_updateid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: c370_s088
--

ALTER SEQUENCE public.website_updateid_seq OWNED BY public.website.updateid;


--
-- Name: campaigns campaignid; Type: DEFAULT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.campaigns ALTER COLUMN campaignid SET DEFAULT nextval('public.campaigns_campaignid_seq'::regclass);


--
-- Name: events eventid; Type: DEFAULT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.events ALTER COLUMN eventid SET DEFAULT nextval('public.events_eventid_seq'::regclass);


--
-- Name: finances transactionid; Type: DEFAULT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.finances ALTER COLUMN transactionid SET DEFAULT nextval('public.finances_transactionid_seq'::regclass);


--
-- Name: members memberid; Type: DEFAULT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.members ALTER COLUMN memberid SET DEFAULT nextval('public.members_memberid_seq'::regclass);


--
-- Name: website updateid; Type: DEFAULT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.website ALTER COLUMN updateid SET DEFAULT nextval('public.website_updateid_seq'::regclass);


--
-- Data for Name: campaignorganizers; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.campaignorganizers (employee, campaignid) FROM stdin;
5	1
6	2
5	3
\.


--
-- Data for Name: campaigns; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.campaigns (campaignid, startdate, enddate, name, description, annotations) FROM stdin;
1	2024-04-01	2024-04-15	Clean Air	Dummy Description 1	\N
2	2024-05-10	2024-07-10	Water Conservation	Dummy Description 2	\N
3	2024-01-20	2024-09-20	Forest PreProtection	Dummy Description 3	\N
4	2024-06-20	2024-08-20	Forest Protection	Dummy Description 4	\N
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.events (eventid, type, date, location, campaignid) FROM stdin;
1	Street Event	2024-04-05	Downtown Square	1
2	Meet and Greet	2024-04-10	City Park	1
3	Walking Protest	2024-05-15	Town Hall	2
4	Street Event	2024-06-25	Community Center	3
\.


--
-- Data for Name: finances; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.finances (transactionid, type, amount, date, campaignid, memberid) FROM stdin;
1	Expense	500.00	2024-04-05	1	\N
2	Donation	1000.00	2024-04-10	1	3
3	Expense	300.00	2024-05-15	2	\N
4	Donation	1500.00	2024-06-25	1	4
5	Rent	2000.00	2024-01-25	\N	\N
6	Salary	1500.00	2024-06-25	\N	5
\.


--
-- Data for Name: memberevents; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.memberevents (member, eventid) FROM stdin;
4	1
3	2
3	3
4	4
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.members (memberid, name, role, tier, numcampaigns, salary, annotations) FROM stdin;
1	John Doe	Volunteer	2	5	\N	\N
2	Jane Smith	Volunteer	1	1	\N	\N
3	Alice Smith	Member	\N	\N	\N	\N
4	Bob Thompson	Member	\N	\N	\N	\N
5	Bob Bobby	Employee	\N	\N	25000.00	\N
6	Tim Bob	Employee	\N	\N	28000.00	\N
\.


--
-- Data for Name: website; Type: TABLE DATA; Schema: public; Owner: c370_s088
--

COPY public.website (updateid, content, phase, date, publishedstatus, campaignid) FROM stdin;
1	Blog Post	Preparation	2024-03-25	f	1
2	Infographic	Active	2024-05-12	t	2
3	Petition	Ongoing	2024-07-01	f	3
\.


--
-- Name: campaigns_campaignid_seq; Type: SEQUENCE SET; Schema: public; Owner: c370_s088
--

SELECT pg_catalog.setval('public.campaigns_campaignid_seq', 4, true);


--
-- Name: events_eventid_seq; Type: SEQUENCE SET; Schema: public; Owner: c370_s088
--

SELECT pg_catalog.setval('public.events_eventid_seq', 4, true);


--
-- Name: finances_transactionid_seq; Type: SEQUENCE SET; Schema: public; Owner: c370_s088
--

SELECT pg_catalog.setval('public.finances_transactionid_seq', 6, true);


--
-- Name: members_memberid_seq; Type: SEQUENCE SET; Schema: public; Owner: c370_s088
--

SELECT pg_catalog.setval('public.members_memberid_seq', 6, true);


--
-- Name: website_updateid_seq; Type: SEQUENCE SET; Schema: public; Owner: c370_s088
--

SELECT pg_catalog.setval('public.website_updateid_seq', 3, true);


--
-- Name: campaignorganizers campaignorganizers_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.campaignorganizers
    ADD CONSTRAINT campaignorganizers_pkey PRIMARY KEY (employee, campaignid);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (campaignid);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (eventid);


--
-- Name: finances finances_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.finances
    ADD CONSTRAINT finances_pkey PRIMARY KEY (transactionid);


--
-- Name: memberevents memberevents_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.memberevents
    ADD CONSTRAINT memberevents_pkey PRIMARY KEY (member, eventid);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (memberid);


--
-- Name: website website_pkey; Type: CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.website
    ADD CONSTRAINT website_pkey PRIMARY KEY (updateid);


--
-- Name: question1 _RETURN; Type: RULE; Schema: public; Owner: c370_s088
--

CREATE OR REPLACE VIEW public.question1 AS
 SELECT c.name AS campaign_name,
    count(e.eventid) AS num_events
   FROM (public.campaigns c
     LEFT JOIN public.events e ON ((c.campaignid = e.campaignid)))
  GROUP BY c.campaignid
  ORDER BY (count(e.eventid)) DESC;


--
-- Name: question2 _RETURN; Type: RULE; Schema: public; Owner: c370_s088
--

CREATE OR REPLACE VIEW public.question2 AS
 SELECT c.name AS campaign_name,
    sum(f.amount) AS total_expenses
   FROM (public.campaigns c
     LEFT JOIN public.finances f ON ((c.campaignid = f.campaignid)))
  WHERE ((f.type)::text = 'Expense'::text)
  GROUP BY c.campaignid;


--
-- Name: question3 _RETURN; Type: RULE; Schema: public; Owner: c370_s088
--

CREATE OR REPLACE VIEW public.question3 AS
 SELECT m.name AS member_name,
    count(me.eventid) AS num_events_participated
   FROM (public.members m
     LEFT JOIN public.memberevents me ON ((m.memberid = me.member)))
  WHERE ((m.role)::text = 'Volunteer'::text)
  GROUP BY m.memberid
  ORDER BY (count(me.eventid)) DESC;


--
-- Name: question5 _RETURN; Type: RULE; Schema: public; Owner: c370_s088
--

CREATE OR REPLACE VIEW public.question5 AS
 SELECT c.name AS campaign_name,
    sum(f.amount) AS total_donations
   FROM (public.campaigns c
     LEFT JOIN public.finances f ON ((c.campaignid = f.campaignid)))
  WHERE ((f.type)::text = 'Donation'::text)
  GROUP BY c.campaignid;


--
-- Name: campaignorganizers campaignorganizers_campaignid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.campaignorganizers
    ADD CONSTRAINT campaignorganizers_campaignid_fkey FOREIGN KEY (campaignid) REFERENCES public.campaigns(campaignid);


--
-- Name: campaignorganizers campaignorganizers_employee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.campaignorganizers
    ADD CONSTRAINT campaignorganizers_employee_fkey FOREIGN KEY (employee) REFERENCES public.members(memberid);


--
-- Name: events events_campaignid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_campaignid_fkey FOREIGN KEY (campaignid) REFERENCES public.campaigns(campaignid);


--
-- Name: finances finances_campaignid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.finances
    ADD CONSTRAINT finances_campaignid_fkey FOREIGN KEY (campaignid) REFERENCES public.campaigns(campaignid);


--
-- Name: finances finances_memberid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.finances
    ADD CONSTRAINT finances_memberid_fkey FOREIGN KEY (memberid) REFERENCES public.members(memberid);


--
-- Name: memberevents memberevents_eventid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.memberevents
    ADD CONSTRAINT memberevents_eventid_fkey FOREIGN KEY (eventid) REFERENCES public.events(eventid);


--
-- Name: memberevents memberevents_member_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.memberevents
    ADD CONSTRAINT memberevents_member_fkey FOREIGN KEY (member) REFERENCES public.members(memberid);


--
-- Name: website website_campaignid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: c370_s088
--

ALTER TABLE ONLY public.website
    ADD CONSTRAINT website_campaignid_fkey FOREIGN KEY (campaignid) REFERENCES public.campaigns(campaignid);


--
-- PostgreSQL database dump complete
--

