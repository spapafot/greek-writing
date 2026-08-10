# Greek Writing

Greek Writing is an agent skill for editing Greek prose. It removes recurring LLM writing patterns while preserving facts, meaning, register, and the author's voice.

The skill is plain Markdown and works with any agent harness that supports skill-style instructions.

## Installation

### Skills CLI

Install globally:

    npx skills add spapafot/greek-writing --global

Update an existing installation:

    npx skills update greek-writing --global

Install for every supported agent harness:

    npx skills add spapafot/greek-writing --global --agent '*'

Omit the global option to install the skill in the current project.

### Claude Code plugin

    /plugin marketplace add spapafot/greek-writing
    /plugin install greek-writing@greek-writing

Invoke the installed plugin with:

    /greek-writing:greek-writing

### Manual installation

Clone the repository into the skills directory used by your agent:

    git clone https://github.com/spapafot/greek-writing.git /path/to/skills/greek-writing

If you already have the repository, copy the runtime file into a skill directory:

    mkdir -p /path/to/skills/greek-writing
    cp SKILL.md /path/to/skills/greek-writing/

## Usage

Paste Greek text after the command:

    /greek-writing

    [Greek text]

You can also request the edit directly:

    Make this sound like natural Greek: [text]

To edit a file:

    Use greek-writing to edit the prose in docs/announcement.md

### Voice matching

Provide two or three paragraphs of your own writing before the text you want edited:

    Use this as a sample of my writing:
    [sample]

    Now edit this text:
    [text]

The sample takes priority over the skill's general style preferences. Greek Writing keeps the author's sentence rhythm, terminology, punctuation habits, and natural quirks.

## How it works

Greek Writing:

- looks for clusters of patterns rather than banning individual words,
- preserves names, numbers, dates, sources, qualifications, and factual claims,
- does not invent details,
- matches the register of the source text,
- teaches every pattern with an original Greek before-and-after pair,
- runs an internal second-pass audit before returning the result.

### 37 patterns

|   # | Pattern                                     | Typical correction                                |
| --: | ------------------------------------------- | ------------------------------------------------- |
|   1 | Inflated significance                       | Keep the concrete fact                            |
|   2 | Unnecessary promotional language            | Remove unsupported praise                         |
|   3 | Vague attribution                           | Name the source or remove the appeal to authority |
|   4 | Chained Greek participles ending in -οντας  | Use direct verbs                                  |
|   5 | Formulaic "challenges and outlook" sections | Keep only specific content                        |
|   6 | Generic optimistic conclusion               | End on the last substantive point                 |
|   7 | Clusters of AI-associated vocabulary        | Simplify the cluster, not every word              |
|   8 | Overuse of «αποτελεί»                       | Prefer «είναι», «έχει», or a direct verb          |
|   9 | "It is not just X, it is Y"                 | State the point directly                          |
|  10 | Mechanical groups of three                  | Keep only the items that matter                   |
|  11 | Unnecessary synonym cycling                 | Repeat the clearest term                          |
|  12 | False ranges                                | Name the topics directly                          |
|  13 | Passive and impersonal syntax               | Name the actor where appropriate                  |
|  14 | Nominalizations                             | Replace them with verbs                           |
|  15 | English idioms translated literally         | Use natural Greek phrasing                        |
|  16 | Overuse of «μέσω» and «με στόχο»            | Use a verb and «για να»                           |
|  17 | The same connector in every paragraph       | Start with the information                        |
|  18 | Over-engineered transitions                 | Let syntax show the relationship                  |
|  19 | Inconsistent technical terminology          | Follow the audience and source text               |
|  20 | Em and en dashes                            | Prefer punctuation natural to the author's Greek  |
|  21 | Excessive bold text                         | Keep only useful emphasis                         |
|  22 | Lists with an inline heading for every item | Use prose when scanning is unnecessary            |
|  23 | Title Case headings                         | Write Greek headings like sentences               |
|  24 | Decorative emoji                            | Remove them unless they belong to the voice       |
|  25 | Mechanical quotation-mark replacement       | Keep one system consistently                      |
|  26 | Chatbot residue                             | Remove conversational scaffolding                 |
|  27 | Speculation used to fill gaps               | State the gap or remove the sentence              |
|  28 | Overly agreeable tone                       | Address the substance directly                    |
|  29 | Filler phrases                              | Tighten them without changing the register        |
|  30 | Excessive hedging                           | Keep one accurate level of uncertainty            |
|  31 | Performative "deeper truth" framing         | Start with the claim                              |
|  32 | Announcing content instead of giving it     | Begin with the subject                            |
|  33 | A heading followed by the same statement    | Remove the empty opening sentence                 |
|  34 | Describing the diff instead of the system   | Explain how the system works now                  |
|  35 | Manufactured drama                          | Combine artificial sentence fragments             |
|  36 | Empty aphorisms                             | Replace them with a concrete claim                |
|  37 | Theatrical "honest" openers                 | Remove the staged hook                            |

## Example

Before:

> Αξίζει να σημειωθεί ότι η νέα πλατφόρμα αποτελεί ένα πραγματικά καινοτόμο εργαλείο, προσφέροντας ταχύτητα, ευελιξία και αξιοπιστία. Παράλληλα, δίνει τη δυνατότητα στις ομάδες να βελτιστοποιήσουν τις διαδικασίες τους, ανοίγοντας τον δρόμο για ένα πιο παραγωγικό μέλλον.

After:

> Η νέα πλατφόρμα βοηθά τις ομάδες να βελτιστοποιήσουν τις διαδικασίες τους.

The rewrite keeps the usable claim, removes unsupported promotional framing, and does not invent a more specific benefit.

## Maintenance

SKILL.md is the source of truth for behavior. If a pattern changes or is renumbered, update the table above in the same change. Keep the version in the plugin manifest synchronized with the version history below.

Run these checks before publishing:

    python scripts/validate-package.py
    npx skills add . --list
    claude plugin validate .

## Credits

Greek Writing was inspired by [blader's Humanizer](https://github.com/blader/humanizer), which introduced the original idea of a portable skill for removing AI-writing patterns.

This project is an independent Greek adaptation. It is not a translation, an official Greek edition, or an affiliated project. Its wording, examples, and pattern guidance focus on problems that appear when LLMs write or translate Greek.

The general detection principles also draw on [Wikipedia's Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## Version history

- **1.1.0** - Added an original Greek before-and-after pair to every pattern and package validation that keeps all 37 pairs present.
- **1.0.0** - Initial release with 37 Greek writing patterns, voice matching, a no-fabrication rule, and portable packaging for agent skills and Claude Code.

## License

MIT
