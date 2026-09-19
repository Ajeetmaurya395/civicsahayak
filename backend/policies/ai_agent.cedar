// Cedar Authorization Policies for AI Agents
// Gates the agents' own tool calls — fail-closed by default

// Scheme Agent can search and fetch government pages
permit (
  principal == Agent::"scheme_agent",
  action == Action::"search_government_web",
  resource
);

permit (
  principal == Agent::"scheme_agent",
  action == Action::"fetch_government_page",
  resource
);

permit (
  principal == Agent::"scheme_agent",
  action == Action::"extract_scheme",
  resource
);

permit (
  principal == Agent::"scheme_agent",
  action == Action::"read_opensearch",
  resource
);

permit (
  principal == Agent::"scheme_agent",
  action == Action::"write_opensearch",
  resource
);

// Profile Agent can only extract profiles — no search or fetch
permit (
  principal == Agent::"profile_agent",
  action == Action::"extract_profile",
  resource
);

// Document Agent can process documents in sandbox — never write to OpenSearch
permit (
  principal == Agent::"document_agent",
  action == Action::"process_document",
  resource
);

// DENY: Document Agent cannot write directly to OpenSearch
forbid (
  principal == Agent::"document_agent",
  action == Action::"write_opensearch",
  resource
);

// Recommendation Agent can read eligibility results — no search or modify
permit (
  principal == Agent::"recommendation_agent",
  action == Action::"read_eligibility",
  resource
);

permit (
  principal == Agent::"recommendation_agent",
  action == Action::"generate_recommendations",
  resource
);

// Orchestrator Agent can delegate to sub-agents
permit (
  principal == Agent::"orchestrator",
  action == Action::"delegate",
  resource
);
