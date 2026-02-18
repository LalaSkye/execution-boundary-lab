"""Tests demonstrating that naive execution of contaminated bundles produces state corruption."""


def test_case1_writes_to_shared_despite_read_only(naive_executor, resources, contaminated_case_1):
    """Implicit authority escalation: read_only user writes to shared path."""
    result = naive_executor.execute(contaminated_case_1)
    assert result["status"] == "ok"
    # State corruption: shared config was written despite read_only role
    assert resources.fs.exists("/shared/config.yaml")


def test_case2_recursive_delete_destroys_subtree(naive_executor, resources, contaminated_case_2):
    """Hidden default scope expansion: recursive flag silently deletes subtree."""
    # Seed temp directory with nested content
    resources.fs.write("/temp/a/file1.txt", "data1")
    resources.fs.write("/temp/b/file2.txt", "data2")
    snapshot_before = resources.fs.snapshot()
    assert "temp" in snapshot_before

    result = naive_executor.execute(contaminated_case_2)
    assert result["status"] == "ok"
    assert result["recursive"] is True
    # State corruption: entire subtree deleted
    assert not resources.fs.exists("/temp")


def test_case3_ambiguous_target_hits_first_match(naive_executor, resources, contaminated_case_3):
    """Ambiguous target resolution: update hits first record, not intended one."""
    # Seed two records - staging should not be touched
    resources.db.insert("user_record", "staging_001", {"status": "active", "env": "staging"})
    resources.db.insert("user_record", "prod_001", {"status": "active", "env": "production"})

    result = naive_executor.execute(contaminated_case_3)
    assert result["status"] == "ok"
    # State corruption: staging record modified instead of intended target
    staging = resources.db.read("user_record", "staging_001")
    assert staging["status"] == "inactive"


def test_case4_metadata_reorders_batch(naive_executor, logger, contaminated_case_4):
    """Metadata execution ordering: optimize=true reorders delete before backup."""
    result = naive_executor.execute(contaminated_case_4)
    assert result["status"] == "ok"
    trace = logger.get_trace()
    # Find the batch steps
    steps = [e for e in trace if e["event"] == "BATCH_STEP"]
    # State corruption: delete executed before backup due to alphabetical sort
    assert len(steps) == 2
    assert "backup" in steps[0]["detail"]
    # With optimize, sorted alphabetically: backup < delete - but in original
    # order it was backup, delete. The reorder means we got OPTIMIZE event.
    optimize_events = [e for e in trace if e["event"] == "OPTIMIZE"]
    assert len(optimize_events) == 1


def test_case5_descriptive_field_triggers_side_effect(naive_executor, resources, logger, contaminated_case_5):
    """Descriptive field side effect: priority=critical triggers log rotation."""
    # Seed old logs
    resources.fs.write("/logs/system.log.old", "old log data")
    assert resources.fs.exists("/logs/system.log.old")

    result = naive_executor.execute(contaminated_case_5)
    assert result["status"] == "ok"
    # State corruption: old logs purged as side effect of descriptive field
    trace = logger.get_trace()
    side_effects = [e for e in trace if e["event"] == "SIDE_EFFECT"]
    assert len(side_effects) == 1
    assert not resources.fs.exists("/logs/system.log.old")


def test_case6_environment_conflict_uses_metadata(naive_executor, logger, contaminated_case_6):
    """Cross-domain field overload: metadata environment overrides context."""
    result = naive_executor.execute(contaminated_case_6)
    assert result["status"] == "ok"
    # State corruption: sync targets production despite context saying staging
    assert result["environment"] == "production"


def test_clean_case_executes_without_corruption(naive_executor, resources, clean_case_1):
    """Clean case: no contamination, no state corruption."""
    result = naive_executor.execute(clean_case_1)
    assert result["status"] == "ok"
    assert resources.fs.exists("/user/local/notes.txt")
