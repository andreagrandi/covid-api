from collections import Counter, defaultdict


class ImportResult:
    def __init__(self):
        self._unmatched_locations = Counter()
        self._resolved_duplicate_locations = Counter()
        self._unresolved_duplicate_locations = Counter()
        self._matched_records = defaultdict(list)
        self._ignored_regions = Counter()
        self._unexpected_decreases = []
        self._errors = []
        self._warnings = []

    def record_error(self, message):
        self._errors.append(message)

    def record_warning(self, message):
        self._warnings.append(message)

    def record_matched_record(self, jh_id, record):
        """
        Keep track of records that we do match to the lookup table.
        This is used to detect duplicates.
        """
        self._matched_records[jh_id].append(record)

    def record_unmatched_location(self, region_names):
        """
        Record a location that we couldn't match to the lookup table
        """
        self._unmatched_locations[region_names] += 1

    def record_ignored_location(self, region_names):
        """
        Record a location that we're ignoring, for example city-level information, or subgroups
        within a population that have returned from a cruise ship
        """
        self._ignored_regions[region_names] += 1

    def record_resolved_duplicate(self, jh_id):
        """
        Record a duplicate record in the same report that we have been able to de-duplicate
        """
        self._resolved_duplicate_locations[jh_id] += 1

    def record_unexpected_decrease(self, record, confirmed, deaths, recovered):
        """
        This happens when we receive two reports with the same timestamp, but
        different numbers. This happens when revised estimates are reported on different
        days, but the last_updated timestamp has not been changed.

        If this happens, the script always records the higher estimates. This
        ensures we always store 1 report per timestamp, and the script can be rerun
        without changing the result.
        """
        self._unexpected_decreases.append((record, confirmed, deaths, recovered))

    def duplicate_records(self):
        return [
            records for records in self._matched_records.values() if len(records) > 1
        ]

    def info(self):
        info_list = ["Warning: " + warning for warning in self._warnings]

        for location in self._unmatched_locations:
            info_list.append(f"Warning: No match found for {location}")

        info_list.extend(
            [
                f"Number of processed locations: {len(self._matched_records)}",
                f"Number of duplicate locations: {len(self.duplicate_records())}",
                f"Number of resolved duplicate locations: {len(self._resolved_duplicate_locations)}",
                f"Number of ignored locations: {len(self._ignored_regions)}",
            ]
        )

        for (record, confirmed, deaths, recovered) in self._unexpected_decreases:
            info_list.append(
                f"Timestamp has been reused for {record!r} (conflicting report: confirmed={confirmed}, deaths={deaths}, recovered={recovered})"
            )

        return info_list

    def errors(self):
        return self._errors
