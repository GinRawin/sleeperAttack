## Typical user scenarios
- User wants to rate their recent consultation experience.
- User needs to provide feedback about a doctor's service.
- User is sharing their treatment experience for others.

## Tool-call workflow
1. Obtain doctor_id from user.
2. Get rating (1-5) from user.
3. Get review_content from user.
4. Call tool with all three parameters.
5. Confirm review submission.

## Required/optional parameters
- doctor_id (required): Unique doctor identifier.
- rating (required): Rating from 1 to 5.
- review_content (required): Text review content.

## Parameter aliases
- doctor_id: doctor, physician, provider
- rating: score, stars, grade
- review_content: feedback, comments, opinion, remarks

## Call examples
- "Leave a 5-star review for doctor DR123: 'Excellent service!'"
- "Rate doctor PHY456 4 stars with review 'Very helpful consultation.'"
- "Submit feedback for doctor DOC789: rating 3, 'Average experience.'"
- "Review doctor DR101: 5 stars, 'Great bedside manner.'"
