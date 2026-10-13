"""Derive identity aliases only from this character's actual source metadata/section.
Never use reference-image subjects, other rows, or shared list defaults.
"""
import re

def derive_aliases(record, root):
    aliases=set(); evidence=[]
    for source in record['sources']:
        text=(root/source['path']).read_text(encoding='utf-8-sig')
        match=re.search(r'^id:\s*([^\r\n]+)',text,re.M)
        source_id=match.group(1).strip().strip('"\'') if match else None
        section=source.get('section')
        if source_id not in [None,'NPC-SCRIPT-CAST','CHAR-N1']:
            if source_id!=record['id']:
                aliases.add(source_id);evidence.append({'alias':source_id,'path':source['path'],'basis':'source frontmatter ID of this character card'})
        elif source_id=='NPC-SCRIPT-CAST':
            if not section or ('## '+section) not in text:
                raise ValueError('Missing exact character section: '+record['id'])
            m=re.search(r'，(NPC-N-[A-Z]+)）$',section)
            if not m:raise ValueError('Missing section character ID: '+record['id'])
            if m[1]!=record['id']:
                aliases.add(m[1]);evidence.append({'alias':m[1],'path':source['path'],'section':section,'basis':'exact selected character section ID'})
        elif source_id=='CHAR-N1':
            # Group-card aliases belong only to their explicitly named table row.
            m=re.search(r'^aliases:\s*\[([^\]]*)\]',text,re.M)
            if m:
                for a in m[1].split(','):
                    a=a.strip().strip('"\'')
                    if a.endswith(record['name']):
                        aliases.add(a);evidence.append({'alias':a,'path':source['path'],'section':section,'basis':'explicit group-card alias matching this named person only'})
    return sorted(aliases),evidence
