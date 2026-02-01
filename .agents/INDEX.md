# 🗂️ AGENT DOCUMENTATION INDEX

**Quick Navigation Guide** | Updated 31/01/2026

---

## 📚 Master Document Map

```
.agents/
├── README.md                              # START HERE - Agent roadmap & execution guide
├── SUMMARY_CONSTRAINT_CLARIFICATION.md    # Overview of all changes (this session)
├── CONSTRAINT_BREAKDOWN.md                # 20 constraints detailed (why, impact, flexibility)
├── CONSTRAINTS.md                         # Master constraint reference table
├── ENVIRONMENT_SETUP.md                   # Setup checklist + blockers + commands
├── agent-1-data-engineer/
│   ├── AGENT_INSTRUCTIONS.md             # Agent 1 detailed mission
│   ├── run.py                            # Agent 1 executor script
│   └── queries.sql                       # Agent 1 validation queries
└── ../
    └── .github/
        └── copilot-instructions.md        # Global AI coding guide

```

---

## 🎯 Find Your Answer

### **"What are the 20 constraints?"**
→ Read: `.agents/CONSTRAINT_BREAKDOWN.md` (full list with "why" each exists)

### **"Can I do X instead of Y?"**
→ Check: `.agents/CONSTRAINTS.md` (flexibility column shows if exception allowed)

### **"How do I set up the environment?"**
→ Follow: `.agents/ENVIRONMENT_SETUP.md` (step-by-step, 3 options provided)

### **"What blocks Agent 1/2/3/4?"**
→ See: `.agents/ENVIRONMENT_SETUP.md` (blocker section per agent)

### **"What's my Agent's specific mission?"**
→ Read: `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (and later agent-2, 3, 4)

### **"What happened in this session?"**
→ Read: `.agents/SUMMARY_CONSTRAINT_CLARIFICATION.md` (recap of all changes)

### **"I need JWT_SECRET right now"**
→ Run: `python -c "import secrets; print(secrets.token_hex(32))"` (or see ENVIRONMENT_SETUP.md)

### **"Can my Agent violate a constraint?"**
→ Check: `CONSTRAINTS.md` column "Flexibility" (ABSOLUTE = no, HARD/MEDIUM = maybe with justification)

### **"Why PostgreSQL + PostGIS and not [X]?"**
→ Read: `.agents/CONSTRAINTS.md` or `.github/copilot-instructions.md` (rationale sections)

### **"Can I run Agent 1 right now?"**
→ Check: `.agents/ENVIRONMENT_SETUP.md` (Agent 1 - BLOCKED section, need DATABASE_URL)

### **"What order should agents run?"**
→ See: `.agents/ENVIRONMENT_SETUP.md` (Optimal execution order: Agent 3 first!)

### **"My Agent needs to access InfinitePay"**
→ Know: It's stand-by until Agent 4. See `.agents/CONSTRAINTS.md` (InfinitePay constraint)

### **"Can I customize JWT expiry from 30min?"**
→ Yes: See `.agents/CONSTRAINT_BREAKDOWN.md` (MEDIUM flexibility, case-by-case)

### **"What files did you update?"**
→ See: `.agents/SUMMARY_CONSTRAINT_CLARIFICATION.md` (files created/modified table)

---

## 🚀 Quick Start Paths

### **Path 1: "I just want to understand constraints"** (15 min)
1. Read: `.agents/README.md` (2 min)
2. Read: `.agents/SUMMARY_CONSTRAINT_CLARIFICATION.md` (5 min)
3. Skim: `.agents/CONSTRAINT_BREAKDOWN.md` (8 min)

### **Path 2: "I need to set up environment"** (30 min)
1. Read: `.agents/ENVIRONMENT_SETUP.md` (5 min)
2. Generate: JWT_SECRET (2 min)
3. Get: DATABASE_URL from Azure Portal (10 min)
4. Run: Validation commands (10 min)
5. Verify: All green ✅ (3 min)

### **Path 3: "I'm running Agent 1"** (20 min)
1. Check: `.agents/ENVIRONMENT_SETUP.md` (Agent 1 - BLOCKED or READY?) (2 min)
2. Read: `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (10 min)
3. Option A: Run `python .agents/agent-1-data-engineer/run.py all` (5 min)
4. Option B: Copy INSTRUCTIONS to Jamba/Copilot for SQL generation (3 min)

### **Path 4: "An Agent wants to violate a constraint"** (10 min)
1. Check: `.agents/CONSTRAINTS.md` (find constraint, read flexibility) (3 min)
2. If ABSOLUTE: No exception, denied (1 min)
3. If HARD: Write trade-off justification (3 min)
4. If MEDIUM: Case-by-case approval (3 min)
5. Document decision (log for future reference) (N/A)

### **Path 5: "I'm Code Reviewing an Agent Output"** (15 min)
1. Get: Agent's output (code/schema/components)
2. Check: `.agents/CONSTRAINT_BREAKDOWN.md` (relevant agent section) (5 min)
3. Verify: Against each applicable constraint (8 min)
4. Document: Pass/Fail with constraint references (2 min)

---

## 📖 Document Purposes

| Document | Purpose | Audience | Read Time |
|----------|---------|----------|-----------|
| `README.md` | Roadmap + how to use agents | Everyone | 5 min |
| `CONSTRAINT_BREAKDOWN.md` | What limits agents + why | Agents, DevOps, PM | 20 min |
| `CONSTRAINTS.md` | Master constraint reference | Agents, Code reviewers | 10 min (reference) |
| `ENVIRONMENT_SETUP.md` | Setup instructions + blockers | DevOps, Backend engineer | 15 min |
| `SUMMARY_CONSTRAINT_CLARIFICATION.md` | Session recap | Project lead | 10 min |
| `agent-1-data-engineer/AGENT_INSTRUCTIONS.md` | Agent 1 specific mission | Agent 1, Code generator | 15 min |
| `.github/copilot-instructions.md` | Global AI coding rules | All AI agents | 20 min |

---

## 🎓 Reading Order by Role

### **Frontend Developer**
1. `.agents/README.md` (overview)
2. `.agents/CONSTRAINT_BREAKDOWN.md` section "Agent 3"
3. `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (understand data schema)
4. → Start coding React components

### **Backend Developer**
1. `.agents/README.md` (overview)
2. `.agents/ENVIRONMENT_SETUP.md` (need JWT_SECRET)
3. `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (understand schema)
4. `.agents/CONSTRAINT_BREAKDOWN.md` section "Agent 2"
5. `.agents/agent-2-backend/AGENT_INSTRUCTIONS.md` (when created)
6. → Start coding Azure Functions

### **Database Engineer**
1. `.agents/README.md` (overview)
2. `.agents/ENVIRONMENT_SETUP.md` (need DATABASE_URL setup)
3. `.agents/CONSTRAINT_BREAKDOWN.md` (understand 20 constraints)
4. `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (your mission)
5. → Execute or send to Jamba for SQL generation

### **DevOps/Infra**
1. `.agents/ENVIRONMENT_SETUP.md` (quick setup, section 2)
2. `.agents/CONSTRAINT_BREAKDOWN.md` (understand blockers)
3. → Deploy resources, set env vars, validate connections

### **Project Manager**
1. `.agents/README.md` (roadmap overview)
2. `.agents/SUMMARY_CONSTRAINT_CLARIFICATION.md` (what changed this session)
3. `.agents/ENVIRONMENT_SETUP.md` (status matrix) → track blockers
4. → Monitor agent progress, unblock as needed

### **AI Code Generator (Jamba/Copilot)**
1. `.github/copilot-instructions.md` (global rules)
2. `.agents/CONSTRAINT_BREAKDOWN.md` (what can/can't do)
3. Specific `.agents/agent-X-*/AGENT_INSTRUCTIONS.md` (your mission)
4. → Generate code/SQL/components per mission

---

## 🔗 Cross-References

**If Agent asks**: "Can I add more tables?"  
→ See: `.agents/CONSTRAINTS.md` row #17, or `.agents/CONSTRAINT_BREAKDOWN.md` section "Agent 1 Extra Tables"

**If Setup blocked**:  
→ See: `.agents/ENVIRONMENT_SETUP.md` section "Blockers for Agent Progress"

**If need to deviate from rules**:  
→ See: `.agents/CONSTRAINTS.md` column "Flexibility" + escalation path in `.agents/CONSTRAINTS.md`

**If confused by architecture**:  
→ See: `.github/copilot-instructions.md` sections "Architecture" + "Business Flow"

**If don't know SRID 4674 requirement**:  
→ See: `.agents/CONSTRAINT_BREAKDOWN.md` section "#4 SRID 4674" or `.agents/CONSTRAINTS.md` rationale

**If JWT_SECRET missing**:  
→ See: `.agents/ENVIRONMENT_SETUP.md` section "Option 2 or 3"

---

## ✅ Completeness Checklist

- [x] All 20 constraints documented
- [x] Setup instructions clear (3 options)
- [x] Blocker analysis per agent
- [x] Rationale for each constraint
- [x] Flexibility levels mapped (Absolute/Hard/Medium/Status)
- [x] Cross-references created
- [x] Quick start paths defined
- [x] Index created (this file)
- [x] Changes summarized (SUMMARY file)

---

## 🎯 Success Criteria

Agents can execute when:
- ✅ Agents read relevant constraint sections
- ✅ Agents understand "why" each constraint exists
- ✅ Agents know when they CAN'T deviate (Absolute)
- ✅ Agents know when they MIGHT be able to (Hard/Medium)
- ✅ Agents know when to escalate (exceptions needed)
- ✅ DevOps has DATABASE_URL + JWT_SECRET set
- ✅ Agents can reference this index when confused

---

**Last Updated**: 31/01/2026

**Questions?** Check this index first → locate → read → done! 🚀

