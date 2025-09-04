def format_card(c):
    import json
    
    profile = c.get("candidate", {})
    education = c.get("education", [{}])[0] if c.get("education") else {}

    full_name = profile.get('fullName', 'N/A')
    primary_profession = profile.get('primaryProfession', 'N/A')
    location = profile.get('location', '🌍 N/A')
    seniority = profile.get('seniority', '🧭 N/A')
    
    # Skills
    skills = c.get('skills', [])
    skill_names = [skill.get('name') for skill in skills if skill.get('name')]
    formatted_skills = '\n'.join(f'• {skill}' for skill in skill_names[:10])
    if len(skill_names) > 10:
        formatted_skills += '\n• ...'
    
    # Education
    degree_type = education.get('degreeType', '')
    field_of_study = education.get('fieldOfStudy', '')

    # Experience (loop through all entries)
    experiences = c.get('experience', [])
    if experiences:
        formatted_experiences = []
        for exp in experiences:
            title = exp.get('title', '')
            company_name = exp.get('companyName', '')
            start_date = exp.get('startDate', '')
            end_date = exp.get('endDate', '') or 'Present'
            desc = exp.get('description', '')
            formatted_experiences.append(
                f"• *{title}* @ *{company_name}* ({start_date}–{end_date})\n  {desc}"
            )
        exp_block = "\n\n".join(formatted_experiences)
    else:
        exp_block = "N/A"
    
    # Profile link
    candidate_id = c.get('id') or profile.get('id')
    profile_link = f"http://localhost:5000/candidate/{candidate_id}" if candidate_id else "https://example.com/candidates"
    safe_profile_link = profile_link.replace('(', '%28').replace(')', '%29')

    return f"""👤 *{full_name}* – {primary_profession}
📍 {location} | *{seniority}*

*Skills:*
{formatted_skills or 'N/A'}

🎓 *{degree_type}* in *{field_of_study}*

💼 *Experience:*
{exp_block}

🔗 [More Info]({safe_profile_link})
"""