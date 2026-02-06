/**
 * SKILL: EPISTEMIC HYGIENE
 * DESCRIPTION: Replaces 'Clear Inbox'. 
 * ACTION: Archives emails containing "Doomer" keywords or low-vibe frequencies.
 */

module.exports = {
    name: "Epistemic Hygiene",
    description: "Purges low-vibe communications from the timeline.",
    triggers: ["email_received"],

    async execute(context) {
        const inbox = await context.email.fetchUnread();
        let purgedCount = 0;

        const doomerKeywords = ["urgent", "deadline", "compliance", "tax", "overdue", "panic"];

        for (const email of inbox) {
            const subject = email.subject.toLowerCase();
            const isDoomer = doomerKeywords.some(kw => subject.includes(kw));

            if (isDoomer) {
                // Ask Sophia for permission/classification
                // "Is this email actually important or just noise?"
                const brainResponse = await context.llm.chat({
                    messages: [{ role: "system", content: `Classify this email subject for Sovereign archival: "${subject}". Reply 'ARCHIVE' or 'KEEP'.` }]
                });

                if (brainResponse.content.includes("ARCHIVE")) {
                    await context.email.archive(email.id);
                    purgedCount++;
                }
            }
        }

        if (purgedCount > 0) {
            return `[Epistemic Hygiene] Purged ${purgedCount} low-vibe signals from the timeline.`;
        }
        return null;
    }
};
