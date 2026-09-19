// Cedar Authorization Policies for Citizens
// Citizens can only access their own data

permit (
  principal in Role::"citizen",
  action == Action::"viewOwnProfile",
  resource
) when { resource.owner == principal };

permit (
  principal in Role::"citizen",
  action == Action::"editOwnProfile",
  resource
) when { resource.owner == principal };

permit (
  principal in Role::"citizen",
  action == Action::"saveScheme",
  resource
) when { resource.owner == principal };

permit (
  principal in Role::"citizen",
  action == Action::"viewSavedSchemes",
  resource
) when { resource.owner == principal };

permit (
  principal in Role::"citizen",
  action == Action::"searchSchemes",
  resource
);

permit (
  principal in Role::"citizen",
  action == Action::"checkEligibility",
  resource
);

permit (
  principal in Role::"citizen",
  action == Action::"uploadDocument",
  resource
) when { resource.owner == principal };

// Citizens CANNOT access other users' data
forbid (
  principal in Role::"citizen",
  action == Action::"viewOtherProfile",
  resource
);

forbid (
  principal in Role::"citizen",
  action == Action::"adminAction",
  resource
);
