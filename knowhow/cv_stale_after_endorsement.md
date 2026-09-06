# Stale cash value after endorsement

## Production symptom

After an endorsement is accepted, the customer portal can still show the prior day's cash value. The user usually reports that the amount is old even though the policy change screen says completed.

## Why it happens

The endorsement transaction publishes an event, while the scheduled recalculation job consumes that event later. If the consumer is delayed or a retry record remains pending, the read model keeps the previous value. This is a timing problem between contract adjustment and the CV calculation batch, not necessarily a failed API request.

## Verification

Check the event id, job execution status, policy version, recalculation timestamp and cache invalidation log. A safe recovery is to reprocess the failed event, rerun the calculation, then invalidate the read cache after the new cash value is committed.

