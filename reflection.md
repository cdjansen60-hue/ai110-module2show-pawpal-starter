# PawPal+ Project Reflection

## 1. System Design

**Three Core Actions**
- Add a pet
- Schedule a task (Task can be broken down into walks, feeding, med, grooming, etc.)
- See today's tasks

**a. Initial design**

My initial design was just Tasks, Pets, and the Schedular. The schedular held the scheduled tasks and the Task objects were time agnostic, with the assumption that the schedular would handle multiple instances of a task object for a different scheduled time/date.

**b. Design changes**

Claude pointed out that later in the assignment that it expects a certain object structure - notably an Owner object (in hindsight, I should have considered this first, I was expecting only one owner per app initially). This changed the hierarchy considerably so that the Schedular no longer owns any data, and instead points to the data held by Owners, Pets, and Tasks respectively.

Upon review of the skeleton by Claude, I chose to update the task relationship to include a reference to the pet it was for. Time strings were updated to be datetime.time objects for validation and ease of sorting. Priority and Frequency were updated to be enum values instead of free strings. A method to get a pet by name through the Owner was also added for future sorting. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
