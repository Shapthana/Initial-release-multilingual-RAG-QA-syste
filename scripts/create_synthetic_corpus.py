from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "data" / "documents"

DOCS_DIR.mkdir(parents=True, exist_ok=True)


DOCUMENTS = {

"university_student_handbook.txt": """
SYNTHETIC DOCUMENT — University Student Handbook
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Student Registration

Students must complete registration before the beginning of each academic semester. Registration requires a valid student identification number and confirmation of the assigned programme. Students who fail to register by the published deadline may need approval from the academic office.

2. Attendance

Students are expected to attend scheduled lectures, laboratories, tutorials and other compulsory academic activities. Individual courses may define additional attendance requirements. Students should consult the relevant course information before the semester begins.

3. Student Identification

Students should carry their university identification card when using laboratories, libraries, examination halls and other restricted facilities. Lost cards should be reported to the student services office.

4. Academic Advising

Each student may consult an assigned academic adviser about course selection, academic progress and general study planning. Advisers do not replace formal approval procedures.

5. Library Access

Registered students may use university library services during published opening hours. Library borrowing privileges depend on the student's account status and applicable library rules.

6. Student Conduct

Students are expected to behave respectfully toward staff and other students. Academic facilities must be used responsibly. Misuse of university systems may be referred to the appropriate disciplinary authority.

7. Communication

Official academic notices are published through designated university communication channels. Students are responsible for checking those channels regularly.

8. Semester Changes

Changes to course registration, programme information or personal records should be submitted through the designated academic office within the published period.

9. Support Services

Students may seek assistance from academic advising, library services, counselling services, career services and student welfare offices.

10. Graduation Clearance

Students approaching graduation must complete academic and administrative clearance requirements before the final certification process.
""",

"course_module_handbook.txt": """
SYNTHETIC DOCUMENT — Course and Module Handbook
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Module Structure

Each module has a module code, title, credit value, learning outcomes and assessment structure. Students should review the module description before selecting a module.

2. Learning Outcomes

Learning outcomes describe the knowledge, skills and abilities expected after successful completion of a module.

3. Assessment

Assessment may include assignments, laboratory work, projects, presentations, quizzes and examinations. The exact weighting is specified in the module information.

4. Coursework Submission

Coursework must normally be submitted through the platform or method specified by the module coordinator. Students should retain evidence of successful submission.

5. Late Work

Late-submission rules are defined by the relevant module. A student who expects difficulty meeting a deadline should contact the coordinator before the deadline where possible.

6. Laboratory Work

Laboratory modules may require preparation before attendance. Students should follow laboratory safety instructions and bring required materials.

7. Group Projects

For group projects, each member is expected to contribute to the assigned work. Assessment may include both group and individual components.

8. Module Feedback

Students may receive written, oral or digital feedback on assessments. Feedback should be used to improve subsequent work.

9. Academic Integrity

Submitted work must represent the student's own permitted contribution. Sources should be acknowledged according to the requirements of the module.

10. Module Completion

Students normally complete a module by satisfying its assessment and participation requirements. Final grades are issued according to the applicable academic regulations.
""",

"library_regulations.txt": """
SYNTHETIC DOCUMENT — Library Regulations
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Opening Hours

The main library is open from 8:00 AM to 10:00 PM on weekdays. Weekend opening is from 9:00 AM to 5:00 PM. Opening hours may change during holidays or examination periods.

2. Borrowing

Eligible students may borrow materials using their valid library identification. Loan periods depend on the material category.

3. Renewals

Eligible materials may be renewed when no reservation has been placed by another user. Renewal requests should be made before the original due date.

4. Returns

Borrowed materials must be returned by the due date. Users should return materials to the designated return point.

5. Overdue Materials

Users with overdue materials may temporarily lose borrowing privileges. Any applicable penalties are determined according to library policy.

6. Reference Materials

Reference-only materials are intended for use within designated library areas unless special permission is granted.

7. Digital Resources

Registered users may access subscribed electronic databases and digital resources according to licence conditions.

8. Library Conduct

Users should maintain a quiet study environment. Food, disruptive behaviour and unauthorized equipment use may be restricted.

9. Lost Materials

A user who loses borrowed material should report the loss to library staff. Replacement or other applicable procedures may follow.

10. Study Rooms

Group study rooms may require advance booking. Users should leave rooms clean and vacate them when their reservation ends.
""",

"examination_regulations.txt": """
SYNTHETIC DOCUMENT — Examination Regulations
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Examination Registration

Students must complete examination registration within the published registration period. Students should verify their registered modules before the deadline.

2. Examination Admission

Students must bring valid identification to an examination. Additional permitted materials are specified in the examination instructions.

3. Arrival

Candidates should arrive before the published examination start time. Late entry is subject to the applicable examination rules.

4. Examination Conduct

Candidates must follow instructions given by authorized examination staff. Communication with other candidates during an examination is prohibited unless explicitly permitted.

5. Electronic Devices

Mobile phones and unauthorized electronic devices must be switched off and stored according to examination instructions.

6. Absence

A student who cannot attend an examination should follow the formal absence procedure and provide required documentation when applicable.

7. Academic Misconduct

Unauthorized assistance, prohibited materials and other forms of examination misconduct may be investigated under academic regulations.

8. Answer Scripts

Candidates must follow instructions for identifying and submitting answer scripts. Scripts must be handed to authorized examination staff before leaving.

9. Results

Examination results are released through designated official channels after the required academic approval process.

10. Appeals

Students who believe an examination decision should be reviewed may use the formal appeal procedure within the specified period.
""",

"scholarship_student_support.txt": """
SYNTHETIC DOCUMENT — Scholarship and Student Support Guide
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Scholarships

Scholarships may support eligible students according to academic, financial, merit-based or other published criteria.

2. Eligibility

Each scholarship has its own eligibility requirements. Students should read the current scholarship notice before applying.

3. Applications

Applications must normally include the information and supporting documents requested in the scholarship announcement.

4. Deadlines

Applications submitted after the stated deadline may not be considered unless the relevant authority announces an extension.

5. Financial Support

Students experiencing financial difficulty may contact the student welfare or support office to learn about available assistance.

6. Accommodation Support

Where accommodation assistance is available, students should apply through the designated student services process.

7. Counselling

Students may seek confidential support from designated counselling services. Appointment procedures are communicated through student support channels.

8. Career Support

Career services may provide guidance on internships, employment preparation, CV development, interviews and career planning.

9. Accessibility

Students who require reasonable academic support should contact the designated support office to discuss available arrangements.

10. Enquiries

Students should use official support-service contact channels for questions about applications, eligibility and deadlines.
""",

"academic_calendar.txt": """
SYNTHETIC DOCUMENT — Academic Calendar
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

Academic Year 2026

1. Registration

Semester 1 registration: 5 January 2026 to 16 January 2026.

2. Semester 1 Teaching

Semester 1 teaching begins on 19 January 2026 and ends on 24 April 2026.

3. Semester 1 Examinations

Semester 1 examinations are scheduled from 4 May 2026 to 22 May 2026.

4. Inter-Semester Break

The inter-semester break is scheduled from 25 May 2026 to 5 June 2026.

5. Semester 2 Registration

Semester 2 registration takes place from 8 June 2026 to 19 June 2026.

6. Semester 2 Teaching

Semester 2 teaching begins on 22 June 2026 and ends on 25 September 2026.

7. Semester 2 Examinations

Semester 2 examinations are scheduled from 5 October 2026 to 23 October 2026.

8. Results

Results are released after completion of the required academic approval procedures. The exact release date may be announced separately.

9. Public Holidays

Teaching and examination schedules may be adjusted when public holidays or officially declared closures affect academic activities.

10. Calendar Updates

Students should consult the latest official calendar notice because dates may be revised by the academic authority.
""",

"research_innovation_policy.txt": """
SYNTHETIC DOCUMENT — Research and Innovation Policy
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Research Principles

Research activities should follow principles of integrity, transparency, responsible conduct and appropriate documentation.

2. Research Proposals

Researchers should prepare proposals that clearly describe objectives, methodology, expected outcomes and resource requirements.

3. Ethics

Research involving human participants, personal data or other regulated subjects may require ethics review before data collection begins.

4. Data Management

Research data should be stored securely and managed according to applicable institutional requirements. Researchers should document important processing decisions.

5. Reproducibility

Researchers are encouraged to maintain versioned code, experiment records, datasets or dataset descriptions and configuration information where appropriate.

6. Publications

Research outputs should accurately acknowledge contributors, supporting institutions and relevant sources.

7. Intellectual Property

Ownership and use of research outputs may depend on institutional agreements, funding conditions and applicable law.

8. Innovation

Innovation projects may be supported through laboratories, mentorship programmes, competitions and collaboration opportunities.

9. Collaboration

External research collaborations should follow applicable approval and agreement procedures.

10. Research Reporting

Researchers may be required to submit progress reports, final reports or other documentation according to the conditions of the relevant project.
""",

"faculty_handbook.txt": """
SYNTHETIC DOCUMENT — Faculty Handbook
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Faculty Administration

Each faculty is supported by academic and administrative offices responsible for programme coordination, student records and academic services.

2. Departments

Departments coordinate teaching, laboratory activities, research and other academic functions within their areas.

3. Programme Coordination

Programme coordinators oversee academic planning and coordinate module information with relevant departments.

4. Laboratory Facilities

Laboratories should be used according to safety procedures and authorized access conditions. Equipment must be handled responsibly.

5. Academic Advising

Departments may assign academic advisers to support students with programme planning and academic progress.

6. Research Groups

Faculty members and students may participate in research groups according to the requirements of the relevant department or project.

7. Seminars

Academic seminars may be organized to share research findings, professional knowledge and technical developments.

8. Student Projects

Departments may establish project guidelines covering supervision, milestones, assessment and submission.

9. Industry Engagement

Faculties may collaborate with external organizations for internships, projects, guest lectures and research activities subject to applicable approval.

10. Administrative Requests

Students should submit faculty-level requests through the designated departmental or faculty office.
""",

"institutional_services_guide.txt": """
SYNTHETIC DOCUMENT — Institutional Services Guide
Created for controlled multilingual RAG evaluation.
NOT an official university publication.

1. Student Services

The student services office assists with general administrative enquiries, student records and selected support requests.

2. Academic Office

The academic office handles programme-related administrative processes, registration matters and selected academic records.

3. Information Technology Services

IT services support university computing facilities, network access and selected digital platforms.

4. Network Accounts

Students may receive institutional credentials for authorized digital services. Credentials should not be shared with other people.

5. Help Desk

Technical problems should be reported through the designated IT help-desk process with sufficient information to identify the problem.

6. Career Services

Career services may provide internship information, employment preparation, CV guidance and career-development activities.

7. Student Welfare

The student welfare office coordinates selected welfare and student-support activities.

8. Accommodation

Accommodation services, where available, operate according to published eligibility and application procedures.

9. Transport

Institutional transport services, where provided, operate according to published routes and schedules.

10. Emergency Contacts

Students should use the designated institutional emergency and security channels when immediate assistance is required.
"""
}


def main():
    print("=" * 70)
    print("CREATING SYNTHETIC RAG CORPUS")
    print("=" * 70)

    created = 0

    for filename, content in DOCUMENTS.items():
        path = DOCS_DIR / filename

        # Do not overwrite your existing original handbook.
        if filename == "sample_multilingual_handbook.txt" and path.exists():
            print(f"Skipping existing file: {filename}")
            continue

        path.write_text(
            content.strip() + "\n",
            encoding="utf-8"
        )

        created += 1
        print(f"Created: {filename}")

    readme = DOCS_DIR / "README_SYNTHETIC_CORPUS.txt"

    readme.write_text(
        """SYNTHETIC MULTILINGUAL INSTITUTIONAL CORPUS

These documents were created specifically for controlled RAG
retrieval experiments.

They are synthetic documents and are NOT official university
regulations, policies, calendars or handbooks.

They should not be presented as real institutional documents.

Purpose:
- BM25 evaluation
- multilingual dense retrieval
- hybrid retrieval
- Reciprocal Rank Fusion
- cross-encoder reranking
- question-type analysis
- controlled RAG benchmarking
""",
        encoding="utf-8"
    )

    print()
    print("=" * 70)
    print(f"Created {created} synthetic documents.")
    print(f"Directory: {DOCS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
    