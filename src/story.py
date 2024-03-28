import random

STORY_SECTION1 = "Opening Image, Setup"
STORY_SECTION2 = "Catalyst, Debate"
STORY_SECTION3 = "Break into Two, B Story, Fun and Games"
STORY_SECTION4 = "Midpoint"
STORY_SECTION5 = "Bad Guys Close In, All Is Lost, Dark Night of the Soul"
STORY_SECTION6 = "Break into Three, Finale"
STORY_SECTION7 = "Final Image"
section_names = [STORY_SECTION1, STORY_SECTION2, STORY_SECTION3, STORY_SECTION4, STORY_SECTION5, STORY_SECTION6, STORY_SECTION7]

monster_in_the_house_prompts_jp = {
STORY_SECTION1: "登場人物たちは、平穏な日常生活を送っていました。しかし、突如としてモンスターの存在が明らかになり、彼らの生活は一変します。モンスターの脅威によって引き起こされる混乱や恐怖、登場人物たちの反応を描写してください。",
STORY_SECTION1: "モンスターの存在が明らかになる衝撃的な出来事が起こり、登場人物たちは大きな影響を受けます。彼らは、この脅威にどう立ち向かうべきか、あるいは逃げるべきかについて議論します。モンスターの脅威や、登場人物たちの不安、緊張感、葛藤を描写しつつ、彼らが決断を下すまでの過程を描いてください。",
STORY_SECTION2: "登場人物たちは、モンスターとの対決を決意し、新たな世界に踏み出します。彼らは問題解決のために奮闘する一方で、自分たちの関係性にも変化が生じます。モンスターの脅威に立ち向かう彼らの勇気と、変化する人間関係のダイナミクスを描写してください。",
STORY_SECTION4: "物語の中盤で、登場人物たちはモンスターに関する衝撃的な事実を発見します。この発見によって状況が一変し、彼らは新たな戦略を迫られます。モンスターの真の姿や目的が明らかになる瞬間と、それによって生じる登場人物たちの心境の変化を描いてください。",
STORY_SECTION5: "モンスターの脅威が差し迫り、登場人物たちは追い詰められます。彼らの計画は失敗に終わり、仲間を失うなど大きな喪失を経験します。絶望的な状況の中で、彼らが自分自身や仲間と向き合う場面を描写してください。",
STORY_SECTION6: "登場人物たちは、これまでの経験から学んだ教訓を生かし、最後の決戦に臨みます。彼らの勇気、犠牲、団結が試される中で、モンスターとの壮絶な戦いを繰り広げます。クライマックスでの激しい戦いと、登場人物たちの成長の瞬間を描写してください。",
STORY_SECTION7: "モンスターとの戦いが終結し、登場人物たちは勝利を収めます。彼らは経験を通じて成長し、新たな絆で結ばれました。平和を取り戻した舞台で、彼らの新しい日常や変化した関係性を描写し、物語を締めくくってください。"
}
monster_in_the_house_prompts = {
STORY_SECTION1: "Introduce a peaceful and serene daily life, followed by an unsettling or anxiety-provoking event. This event is a glimpse of the presence that threatens the characters, though they are not yet aware of it. Describe the introduction of the story, raising the question of how long their daily life will continue within the confined space.",
STORY_SECTION2: "The presence of the monster becomes apparent, greatly impacting the characters. They debate whether to confront this threat or flee from it. Depict the characters' anxiety, tension, and conflict leading up to their decision, along with the process of describing the threat of the monster.",
STORY_SECTION3: "The characters decide to confront the monster and venture into a new world. While they strive to solve the problem, their relationships also undergo changes. Portray the characters' courage in facing the monster's threat and the dynamics of their changing human relationships.",
STORY_SECTION4: "The characters make a shocking discovery about the monster in the middle of the story. This discovery changes the situation, and they are forced to adopt a new strategy. Describe the moment the monster's true nature or purpose is revealed and the change in the characters' state of mind.",
STORY_SECTION5: "The monster's threat looms large, and the characters are cornered. Their plans fail, and they experience significant losses, such as losing companions. Depict the characters' desperate situation and their search for a way to recover amidst hopelessness.",
STORY_SECTION6: "The characters draw upon the lessons learned from their experiences and confront the monster in a final battle. They engage in a fierce struggle, putting their courage, sacrifice, and unity to the test. Describe the characters' exploits in the climax and the moment of their growth.",
STORY_SECTION7: "The battle with the monster concludes, and the characters emerge victorious. They have grown through their experiences and are bound by new ties. Portray the characters' new daily life in the peaceful setting, their changed relationships, and conclude the story."
}


golden_fleece_prompts_jp = {
STORY_SECTION1: "主人公の現在の生活と、彼らが抱える問題や欠点を紹介します。そして、主人公が何かを求めて冒険に出るきっかけとなる出来事が起こります。主人公のキャラクター性や環境設定、そして冒険への期待感を描写してください。",
STORY_SECTION2: "主人公は冒険に出ることを決意しますが、同時に不安や葛藤も抱えています。周囲の人々は主人公の決定に対して様々な反応を示します。主人公が冒険に出る決意を固めるまでの心の動きと、周囲の反応を描写してください。",
STORY_SECTION3: "主人公は冒険の世界に飛び込み、新たな仲間や敵と出会います。彼らは目的達成のために様々な困難に立ち向かいます。主人公が新しい環境に適応していく過程と、仲間との絆の深まりを描写してください。",
STORY_SECTION4: "冒険の途中で、主人公は自分の目的や能力について新たな発見をします。この発見によって、主人公の視点や行動が大きく変化します。主人公の成長の瞬間と、それによってもたらされる物語の転換点を描写してください。",
STORY_SECTION5: "主人公は最大の試練に直面し、目的達成が絶望的に思えます。仲間との衝突や裏切りなども経験し、孤独と絶望感に苛まれます。主人公が最も低い状態に陥る様子と、そこから立ち上がる決意を描写してください。",
STORY_SECTION6: "主人公は試練を乗り越え、自分自身と向き合った結果、新たな強さを手に入れます。彼らは最終的な目的に向かって行動を起こし、困難な状況でも勇気と知恵を発揮します。クライマックスでの主人公の活躍と、目的達成の瞬間を描写してください。",
STORY_SECTION7: "主人公は冒険を通じて成長し、新たな自分を受け入れます。彼らは冒険で得たものを持って日常生活に戻り、周囲の人々との関係性にも変化が生じます。主人公の成長と変化した環境を描写し、冒険の意義を述べて物語を締めくくってください。"
}
golden_fleece_prompts = {
STORY_SECTION1: "Introduce the protagonist's current life, the problems or flaws they face, and the event that triggers their journey. The protagonist's character and environment are described, along with their anticipation of the adventure.",
STORY_SECTION2: "The protagonist decides to embark on the adventure but simultaneously harbors anxiety and internal conflict. The people around the protagonist react in various ways to their decision. Depict the protagonist's emotional journey leading to their determination to set out on the adventure and the reactions of others.",
STORY_SECTION3: "The protagonist embarks on the adventure and encounters new allies and enemies. They face various difficulties and obstacles to achieve their goal. Portray the protagonist's process of adapting to the new environment and the deepening of their bonds with their companions.",
STORY_SECTION4: "During the adventure, the protagonist makes a significant discovery about their goals or abilities. This discovery greatly changes the protagonist's perspective and actions. Describe the moment of the protagonist's growth and the turning point it brings to the story.",
STORY_SECTION5: "The protagonist faces their greatest trial and feels the limits of their abilities. They experience failure, lose companions, or suffer other significant losses. Depict the protagonist at their lowest point and their search for a way to recover.",
STORY_SECTION6: "The protagonist overcomes the trials and gains new strength and wisdom. They take final action towards their ultimate goal, displaying courage and determination in the face of adversity. Describe the protagonist's exploits in the climax and the moment they achieve their goal.",
STORY_SECTION7: "The protagonist completes the adventure and accepts their new self. They return to their daily life with the experiences and growth gained from the adventure. Portray the protagonist's growth, the changes in their environment, and conclude the story by discussing the significance of the adventure."
}

out_of_the_bottle_prompts_jp = {
STORY_SECTION1: "主人公の日常生活と、彼らが抱える不満や欲求を描写します。そして、主人公が何らかの魔法や超常現象に触れ、願いを叶えるチャンスを得ます。主人公のキャラクター性や環境設定、そして願いへの期待感を描写してください。",
STORY_SECTION2: "主人公は願いを叶えることを決意しますが、同時に不安や葛藤も抱えています。周囲の人々は主人公の決定に対して警告や懸念を示します。主人公が願いを実現する決意を固めるまでの心の動きと、周囲の反応を描写してください。",
STORY_SECTION3: "主人公の願いが叶えられ、新たな現実が生まれます。当初は願いの成就を楽しむ主人公ですが、徐々に予期せぬ問題が発生し始めます。主人公が新しい現実に適応していく過程と、願いの真の代償に気づき始める様子を描写してください。",
STORY_SECTION4: "願いによってもたらされた問題が深刻化し、主人公は現実世界への影響の大きさを理解します。この発見によって、主人公は願いの取り消しを検討し始めます。主人公の心境の変化と、物語の転換点を描写してください。",
STORY_SECTION5: "願いがもたらした問題が主人公や周囲の人々を圧倒し、状況は最悪の事態を迎えます。主人公は自分の選択の誤りと無力感に苛まれ、絶望的な状況に陥ります。主人公が最も低い状態に陥る様子と、問題解決への模索を描写してください。",
STORY_SECTION6: "主人公は自分の過ちを認め、問題解決のために行動を起こします。彼らは願いを取り消すための方法を見つけ出し、勇気と決断力を持ってそれを実行します。クライマックスでの主人公の選択と、願いの取り消しの瞬間を描写してください。",
STORY_SECTION7: "願いが取り消され、現実世界は元の状態に戻ります。主人公は経験を通じて成長し、自分の欲求と現実との向き合い方を学びます。主人公の成長と、経験から得られた教訓を述べて物語を締めくくってください。"
}
out_of_the_bottle_prompts = {
STORY_SECTION1: "Introduce the protagonist's daily life and the dissatisfaction or desires they harbor. The protagonist encounters magic or supernatural phenomena and gets a chance to have their wishes granted. Describe the protagonist's character and their anticipation of the wish.",
STORY_SECTION2: "The protagonist decides to make the wish but simultaneously harbors anxiety and internal conflict. Those around the protagonist warn them or express concerns about their decision. Depict the protagonist's emotional journey leading to their determination to realize the wish and the reactions of others.",
STORY_SECTION3: "The protagonist's wish is granted, and a new reality emerges. Initially, the protagonist enjoys the fulfillment of their wish, but unexpected problems gradually begin to occur. Portray the protagonist's process of adapting to the new reality and their growing awareness of the true cost of the wish.",
STORY_SECTION4: "The problems caused by the wish escalate, and the protagonist realizes the magnitude of the wish's impact on the real world. The protagonist begins to consider revoking the wish. Describe the change in the protagonist's state of mind and the turning point in the story.",
STORY_SECTION5: "The problems brought about by the wish overwhelm the protagonist, and the situation reaches a critical point. The protagonist is plagued by a sense of powerlessness and despair, finding themselves in a desperate situation. Depict the protagonist at their lowest point and their search for a way to solve the problem.",
STORY_SECTION6: "The protagonist acknowledges their mistake and takes action to resolve the problem. They find a way to revoke the wish and courageously carry it out. Describe the protagonist's choice in the climax and the moment the wish is revoked.",
STORY_SECTION7: "The wish is revoked, and the real world returns to its original state. The protagonist grows and learns to accept their desires and reality. Portray the protagonist's growth, the lessons learned from the experience, and conclude the story."
}

dude_with_a_problem_prompts_jp = {
STORY_SECTION1: "主人公の日常生活と、彼らが抱える個人的な問題や欠点を描写します。そして、主人公が予期せぬ事件や危機に巻き込まれる様子を提示します。主人公のキャラクター性や環境設定、そして問題の深刻さを描写してください。",
STORY_SECTION2: "主人公は問題解決のために行動を起こすことを決意しますが、同時に不安や葛藤も抱えています。周囲の人々は主人公の決定に対して様々な反応を示します。主人公が行動を起こす決意を固めるまでの心の動きと、周囲の反応を描写してください。",
STORY_SECTION3: "主人公は問題解決のために奮闘し、予期せぬ障害や新たな問題に直面します。彼らは問題の本質を理解するために、様々な手がかりを追います。主人公が問題解決に向けて努力する過程と、問題の複雑さが明らかになっていく様子を描写してください。",
STORY_SECTION4: "主人公は問題の核心に迫る重要な発見をします。この発見によって、主人公の理解が深まると同時に、問題解決への新たな障害が明らかになります。主人公の心境の変化と、物語の転換点を描写してください。",
STORY_SECTION5: "問題が主人公を圧倒し、状況は最悪の事態を迎えます。主人公は自分の無力感と絶望感に苛まれ、問題解決への希望を失います。主人公が最も低い状態に陥る様子と、問題解決への新たな糸口を模索する過程を描写してください。",
STORY_SECTION6: "主人公は新たな視点や助けを得て、問題解決への最後の手段を見出します。彼らは勇気と決意を持って行動を起こし、困難な状況に立ち向かいます。クライマックスでの主人公の奮闘と、問題解決の瞬間を描写してください。",
STORY_SECTION7: "問題が解決され、主人公は経験を通じて成長します。彼らは問題解決の過程で得た教訓を活かし、新たな人生を歩み始めます。主人公の成長と、経験がもたらした変化を描写し、物語を締めくくってください。"
}
dude_with_a_problem_prompts = {
STORY_SECTION1: "Introduce the protagonist's daily life and the personal problems or flaws they face. Present the unexpected incident or crisis that the protagonist becomes involved in. Describe the protagonist's character and the seriousness of the problem.",
STORY_SECTION2: "The protagonist decides to take action to solve the problem but simultaneously harbors anxiety and internal conflict. Those around the protagonist react in various ways to their decision. Depict the protagonist's emotional journey leading to their determination to take action and the reactions of others.",
STORY_SECTION3: "The protagonist begins to strive to solve the problem and faces unexpected obstacles and new challenges. They pursue various clues to understand the essence of the problem. Portray the protagonist's efforts to solve the problem and the increasing complexity of the situation.",
STORY_SECTION4: "The protagonist makes a significant discovery that brings them closer to the core of the problem. This discovery sheds new light on the situation but also reveals new obstacles. Describe the protagonist's discovery and the turning point in the story.",
STORY_SECTION5: "The problem overwhelms the protagonist, and the situation reaches its worst point. The protagonist feels helpless and questions their ability to solve the problem. Depict the protagonist at their lowest point and their search for a new way to solve the problem.",
STORY_SECTION6: "The protagonist gains a new perspective or assistance and takes final action to solve the problem fundamentally. They display courage and determination in the face of difficult situations. Describe the protagonist's exploits in the climax and the moment the problem is solved.",
STORY_SECTION7: "The problem is solved, and the protagonist grows through their experiences. They apply the lessons learned from solving the problem and begin a new life. Portray the protagonist's growth, the changes brought about by the experience, and conclude the story."
}

rites_of_passage_prompts_jp = {
STORY_SECTION1: "主人公の現在の状況と、彼らが属するコミュニティや文化について描写します。そして、主人公が人生の転換期に差し掛かり、通過儀礼に直面することを示唆します。主人公のキャラクター性や環境設定、そして通過儀礼への期待感を描写してください。",
STORY_SECTION2: "主人公は通過儀礼に臨むことを決意しますが、同時に不安や葛藤も抱えています。周囲の人々は主人公に対して様々なアドバイスや期待を寄せます。主人公が通過儀礼に臨む決意を固めるまでの心の動きと、周囲の反応を描写してください。",
STORY_SECTION3: "主人公は通過儀礼の過程で、様々な試練や課題に直面します。彼らは自分自身と向き合い、成長するために努力します。主人公が試練を乗り越えていく過程と、自己発見や新たな関係性の形成を描写してください。",
STORY_SECTION4: "主人公は通過儀礼の過程で、自分自身や周囲の世界について重要な洞察を得ます。この発見によって、主人公の視点や価値観が大きく変化します。主人公の成長の瞬間と、それによってもたらされる物語の転換点を描写してください。",
STORY_SECTION5: "主人公は通過儀礼の最大の試練に直面し、自分の限界や弱さと向き合います。彼らは失敗や挫折を経験し、自信を失います。主人公が最も低い状態に陥る様子と、そこから立ち上がる決意を描写してください。",
STORY_SECTION6: "主人公は試練を乗り越え、新たな強さと知恵を獲得します。彼らは通過儀礼の最終段階に臨み、自分の成長を証明します。クライマックスでの主人公の勝利と、通過儀礼の完了の瞬間を描写してください。",
STORY_SECTION7: "主人公は通過儀礼を終え、新たな自分として生まれ変わります。彼らはコミュニティの一員として認められ、新たな役割を担います。主人公の成長と変化、そして通過儀礼の意義を描写し、物語を締めくくってください。"
}
rites_of_passage_prompts = {
STORY_SECTION1: "Introduce the protagonist's current situation and the community or culture they belong to. Indicate that the protagonist is approaching a turning point in their life and facing a rite of passage. Describe the protagonist's character and their anticipation of the rite of passage.",
STORY_SECTION2: "The protagonist resolves to undergo the rite of passage but simultaneously harbors anxiety and internal conflict. People around the protagonist offer various advice and expectations. Depict the protagonist's emotional journey leading to their determination to face the rite of passage and the reactions of those around them.",
STORY_SECTION3: "The protagonist faces various trials and challenges in the process of the rite of passage. They confront themselves and strive to grow. Describe the protagonist's process of overcoming trials, self-discovery, and the formation of new relationships.",
STORY_SECTION4: "The protagonist gains a significant insight into themselves and the world around them during the rite of passage. This discovery greatly changes the protagonist's perspective and values. Portray the moment of the protagonist's growth and the turning point it brings to the story.",
STORY_SECTION5: "The protagonist faces the greatest trial of the rite of passage and confronts their own limitations and weaknesses. They experience failure and setbacks, losing confidence in themselves. Depict the protagonist at their lowest point and their search for a way to recover.",
STORY_SECTION6: "The protagonist overcomes the trials and gains new strength and wisdom. They face the final stage of the rite of passage and prove their growth. Describe the protagonist's triumph in the climax and the moment of completing the rite of passage.",
STORY_SECTION7: "Having finished the rite of passage, the protagonist is reborn as a new self. They are recognized as a member of the community and take on a new role. Portray the protagonist's growth, the changes brought about by the rite of passage, and conclude the story."
}

buddy_love_prompts_jp = {
STORY_SECTION1: "二人の主人公の性格や背景、そして二人の出会いのシーンを描写します。主人公たちは性格や考え方が対照的で、最初は衝突したり反発し合ったりします。二人の主人公のキャラクター性と、出会いの状況を描写してください。",
STORY_SECTION2: "主人公たちは何らかの理由で一緒に行動することを余儀なくされます。二人は協力することに消極的で、互いの違いを強調し合います。主人公たちが協力を決意するまでの議論と、その過程で明らかになる二人の価値観の違いを描写してください。",
STORY_SECTION3: "主人公たちは共通の目的に向かって行動し始めます。二人は様々な困難や障害に直面しながらも、徐々にお互いを理解し、尊重し合うようになります。主人公たちの関係の変化と、共に成長していく過程を描写してください。",
STORY_SECTION4: "主人公たちは互いに深い信頼関係を築きますが、同時に新たな問題や衝突が生じます。二人の関係が試される中で、それぞれが自分自身と向き合う必要性に気づきます。主人公たちの関係の転換点と、内面的な成長の始まりを描写してください。",
STORY_SECTION5: "主人公たちの関係は最大の危機を迎えます。互いの信頼が揺らぎ、二人の絆は崩壊の危機に瀕します。主人公たちが最も低い状態に陥る様子と、関係修復への模索を描写してください。",
STORY_SECTION6: "主人公たちは互いの大切さを再認識し、関係を修復するために行動を起こします。二人は困難を乗り越え、より強い絆で結ばれます。クライマックスでの主人公たちの再会と、関係の深まりを描写してください。",
STORY_SECTION7: "主人公たちは経験を通じて成長し、互いに欠かせない存在となります。二人は新たな関係性の中で、それぞれの人生を歩んでいきます。主人公たちの成長と、深まった絆を描写し、物語を締めくくってください。"
}
buddy_love_prompts = {
STORY_SECTION1: "Introduce the two main characters, their personalities, backgrounds, and the scene of their first encounter. The main characters have contrasting personalities and ideas, initially clashing and repelling each other. Describe the main characters' characteristics and the circumstances of their meeting.",
STORY_SECTION2: "The main characters are forced to work together for some reason. They are reluctant to cooperate and emphasize their differences. Describe the argument leading up to their decision to work together and the differences in their values that become apparent in the process.",
STORY_SECTION3: "The main characters begin to act towards a common goal. Despite facing various difficulties and obstacles, they gradually come to understand and respect each other. Portray the changes in the main characters' relationship and their process of growing together.",
STORY_SECTION4: "The main characters build a deep trust in each other, but at the same time, new problems or conflicts arise. Amidst the testing of their relationship, they each realize the need to confront their own issues. Describe the turning point in the main characters' relationship and the beginning of their internal growth.",
STORY_SECTION5: "The main characters' relationship faces its greatest crisis. Their trust in each other wavers, and their bond is on the verge of collapse. Depict the main characters at their lowest point and their search for a way to mend their relationship.",
STORY_SECTION6: "The main characters recognize each other's importance and take action to repair their relationship. They overcome difficulties and become connected by a stronger bond. Describe the main characters' reunion in the climax and the deepening of their relationship.",
STORY_SECTION7: "The main characters have grown through their experiences and become indispensable to each other. They walk their respective paths in life within a new relationship. Portray the main characters' growth and their deepened bond, concluding the story."
}

whydunit_prompts_jp = {
STORY_SECTION1: "事件や謎の発生と、その影響を受ける登場人物たちを描写します。読者は事件の真相や動機に興味を持ちますが、それが明らかにされるのは物語の最後になります。事件の概要と、登場人物たちの関係性を描写してください。",
STORY_SECTION2: "主人公（探偵や刑事など）が事件の調査を開始します。他の登場人物たちは事件について様々な憶測や意見を述べます。主人公が本格的な調査を開始するまでの経緯と、登場人物たちの反応を描写してください。",
STORY_SECTION3: "主人公は事件の真相を追求するために、手がかりを集めたり、関係者に質問したりします。調査の過程で、新たな事実や矛盾点が明らかになります。主人公の調査の進展と、浮上する謎を描写してください。",
STORY_SECTION4: "主人公は事件の核心に迫る重要な発見をします。この発見によって、事件の全体像が見え始めますが、同時に新たな謎も生まれます。主人公の発見と、物語の転換点を描写してください。",
STORY_SECTION5: "主人公の調査は行き詰まり、真相は依然として闇の中にあります。主人公は自分の推理や判断力に疑問を抱き、絶望的な状況に陥ります。主人公が最も低い状態に陥る様子と、真相解明への新たな糸口を模索する過程を描写してください。",
STORY_SECTION6: "主人公は新たな発見や洞察によって、事件の全容を把握します。真相と犯人の動機が明らかになり、すべての謎が解き明かされます。クライマックスでの主人公の推理と、真相の露呈の瞬間を描写してください。",
STORY_SECTION7: "事件が解決され、登場人物たちは真相を受け入れます。犯人の動機が明らかになることで、事件の意味や教訓が浮き彫りになります。事件の余波と、登場人物たちの変化を描写し、物語を締めくくってください。"
}
whydunit_prompts = {
STORY_SECTION1: "Describe the occurrence of a crime or mystery and its impact on the characters. The reader is intrigued by the truth behind the incident and the motive, which will be revealed at the end of the story. Outline the crime and the relationships between the characters.",
STORY_SECTION2: "The protagonist (detective or investigator) begins to investigate the case. Other characters offer various speculations and opinions about the incident. Describe the events leading up to the protagonist's decision to start a full-fledged investigation and the reactions of the other characters.",
STORY_SECTION3: "The protagonist gathers clues and questions relevant parties to uncover the truth behind the case. New facts and inconsistencies come to light during the investigation. Portray the progress of the protagonist's investigation and the emerging mysteries.",
STORY_SECTION4: "The protagonist makes a significant discovery that brings them closer to the core of the case. This discovery sheds light on the bigger picture, but it also raises new questions. Describe the protagonist's discovery and the turning point in the story.",
STORY_SECTION5: "The protagonist's investigation hits a dead end, and the truth remains hidden in the darkness. The protagonist doubts their own deductions and judgment, finding themselves in a desperate situation. Depict the protagonist at their lowest point and their search for a new lead to unravel the truth.",
STORY_SECTION6: "With new findings and insights, the protagonist grasps the entire picture of the case. The truth and the culprit's motive are revealed, and all the mysteries are solved. Describe the protagonist's deductions in the climax and the moment the truth is exposed.",
STORY_SECTION7: "The case is solved, and the characters come to terms with the truth. The culprit's motive becomes clear, highlighting the meaning and lessons of the incident. Portray the aftermath of the case and the changes in the characters, concluding the story by discussing the significance of the incident."
}

fool_triumphant_prompts_jp = {
STORY_SECTION1: "一見愚かで取るに足りない主人公が登場し、その性格や環境が描写されます。主人公は周囲から過小評価されていますが、実は豊かな内面や隠れた才能を持っています。主人公のキャラクター性と、周囲との関係性を描写してください。",
STORY_SECTION2: "主人公は何らかの問題や困難に直面します。周囲の人々は主人公の能力を信じておらず、主人公自身も自信を持てずにいます。主人公が問題解決に乗り出すまでの葛藤と、周囲の反応を描写してください。",
STORY_SECTION3: "主人公は独自の方法で問題解決に取り組み始めます。一見奇抜で愚かに見える主人公の行動は、実は問題の核心を突いていることが徐々に明らかになります。主人公の奮闘ぶりと、周囲の評価の変化を描写してください。",
STORY_SECTION4: "主人公の行動が功を奏し、問題解決への道筋が見え始めます。主人公の能力が認められ始め、自信も芽生えてきます。主人公の成長の瞬間と、物語の転換点を描写してください。",
STORY_SECTION5: "主人公は最大の危機に直面します。問題が思わぬ方向に発展し、主人公の能力だけでは対処できない状況に陥ります。主人公が最も低い状態に陥る様子と、問題解決への新たな糸口を模索する過程を描写してください。",
STORY_SECTION6: "主人公は自分の真の強みを発揮し、ユニークな方法で問題を解決します。主人公の創意工夫と勇気が功を奏し、周囲の人々も主人公の価値を認めます。クライマックスでの主人公の活躍と、問題解決の瞬間を描写してください。",
STORY_SECTION7: "主人公は問題を解決し、周囲から称賛されます。主人公の成長と、周囲との関係性の変化が描写されます。主人公の勝利と、物語の教訓を示して、物語を締めくくってください。"
}
fool_triumphant_prompts = {
STORY_SECTION1: "Introduce the seemingly foolish and insignificant protagonist, describing their character and environment. The protagonist is underestimated by others but possesses a rich inner world and hidden talents. Depict the protagonist's character and their relationships with others.",
STORY_SECTION2: "The protagonist faces a problem or difficulty. Those around them don't believe in the protagonist's abilities, and the protagonist themselves lacks confidence. Describe the protagonist's inner conflict leading to their determination to solve the problem and the reactions of others.",
STORY_SECTION3: "The protagonist begins to tackle the problem in their own unique way. The protagonist's seemingly bizarre and foolish actions actually start to get to the heart of the problem, which gradually becomes apparent. Portray the protagonist's struggles and the change in others' perceptions.",
STORY_SECTION4: "The protagonist's actions begin to bear fruit, and a path to solving the problem becomes visible. The protagonist's abilities start to be recognized, and their self-confidence grows. Describe the moment of the protagonist's growth and the turning point in the story.",
STORY_SECTION5: "The protagonist faces their greatest crisis. The problem takes an unexpected turn, and the situation becomes unmanageable for the protagonist alone. Depict the protagonist at their lowest point and their search for a new way to solve the problem.",
STORY_SECTION6: "The protagonist showcases their true strengths and solves the problem in a unique way. The protagonist's creativity and courage pay off, and others recognize the protagonist's value. Describe the protagonist's exploits in the climax and the moment the problem is solved.",
STORY_SECTION7: "The protagonist solves the problem and receives praise from others. The protagonist's growth and changes in their relationships with others are portrayed. Indicate the protagonist's victory, the lessons learned from the story, and conclude the narrative."
}
institutionalized_prompts_jp = {
STORY_SECTION1: "主人公が閉鎖的な組織やコミュニティに属していることを示します。主人公は組織の規則や慣習に縛られ、自由を制限されています。主人公のキャラクター性と、組織の特徴を描写してください。",
STORY_SECTION2: "主人公は組織の問題点や矛盾に気づき始めます。主人公は現状に疑問を抱きますが、同時に組織への帰属意識や恐怖心も抱いています。主人公が変革を決意するまでの葛藤と、周囲の反応を描写してください。",
STORY_SECTION3: "主人公は組織の問題点を解決するために行動を起こし始めます。主人公は同じ思いを持つ仲間を集め、組織の権威に立ち向かいます。主人公の行動と、組織側の対応を描写してください。",
STORY_SECTION4: "主人公の行動が功を奏し、組織内に変化の兆しが見え始めます。しかし同時に、組織側の抵抗も強まります。主人公の成果と、新たな障害の出現を描写してください。",
STORY_SECTION5: "組織側の巻き返しにより、主人公は追い詰められます。主人公は孤立無援の状態に陥り、自分の行動に疑問を抱き始めます。主人公が最も低い状態に陥る様子と、立ち直るための模索を描写してください。",
STORY_SECTION6: "主人公は新たな決意を持って立ち上がり、組織の問題点を根本から解決するための最終的な行動を起こします。主人公の行動が組織を変革へと導きます。クライマックスでの主人公の活躍と、組織の変革の瞬間を描写してください。",
STORY_SECTION7: "組織が変革を遂げ、主人公と仲間たちは自由を獲得します。組織の変化と、主人公の成長を描写してください。新しい組織のあり方と、主人公の役割を示して、物語を締めくくってください。"
}
institutionalized_prompts = {
STORY_SECTION1: "Introduce the protagonist as a member of a closed organization or community. The protagonist is bound by the organization's rules and customs, limiting their freedom. Describe the protagonist's character and the characteristics of the organization.",
STORY_SECTION2: "The protagonist begins to notice problems and contradictions within the organization. They question the current situation but simultaneously feel a sense of belonging and fear towards the organization. Depict the protagonist's internal conflict leading to their determination to bring about change, and the reactions of those around them.",
STORY_SECTION3: "The protagonist starts taking action to solve the organization's problems. They gather allies who share the same thoughts and confront the organization's authority. Describe the protagonist's actions and the organization's response.",
STORY_SECTION4: "The protagonist's actions begin to show signs of change within the organization. However, at the same time, resistance from the organization intensifies. Portray the protagonist's achievements and the emergence of new obstacles.",
STORY_SECTION5: "The organization's counterattack puts the protagonist in a tough spot. The protagonist finds themselves isolated and starts to question their own actions. Depict the protagonist's lowest point and their search for a way to recover.",
STORY_SECTION6: "With renewed determination, the protagonist rises to take final action to solve the organization's problems at their root. The protagonist's actions lead the organization to reform. Describe the protagonist's exploits in the climax and the moment of organizational change.",
STORY_SECTION7: "The organization undergoes reform, and the protagonist and their allies gain freedom. Depict the changes in the organization and the protagonist's growth. Indicate the new state of the organization, the protagonist's role, and conclude the story."
}

superhero_prompts_jp = {
STORY_SECTION1: "主人公（ヒーロー）の日常生活と、彼らが持つ特殊な能力や使命感を描写します。ヒーローは普通の生活を送りながらも、人々を守るために活動しています。ヒーローのキャラクター性と、彼らを取り巻く世界観を描写してください。",
STORY_SECTION2: "重大な脅威や敵の存在が明らかになります。ヒーローは自分の能力で対処すべきか、普通の生活を優先すべきか葛藤します。ヒーローが敵に立ち向かう決意をするまでの心の動きと、周囲の反応を描写してください。",
STORY_SECTION3: "ヒーローは敵に立ち向かうために行動を開始します。ヒーローは自分の能力を駆使して敵と戦いますが、同時に個人的な問題や人間関係の challenges にも直面します。ヒーローの活躍と、彼らの内面的な成長を描写してください。",
STORY_SECTION4: "ヒーローは敵との戦いで重要な勝利を収めますが、同時に新たな脅威や問題が明らかになります。ヒーローは自分の能力や役割について新たな認識を得ます。物語の転換点と、ヒーローの心境の変化を描写してください。",
STORY_SECTION5: "敵が圧倒的な力を見せつけ、ヒーローは危機的な状況に陥ります。ヒーローは自分の能力に限界を感じ、使命を果たせないのではないかと不安になります。ヒーローが最も低い状態に陥る様子と、立ち直るための模索を描写してください。",
STORY_SECTION6: "ヒーローは新たな力や洞察を得て、最終的な敵との対決に臨みます。ヒーローは自分の能力と仲間の助けを借りて、敵を打ち負かします。クライマックスでのヒーローの活躍と、敵の敗北の瞬間を描写してください。",
STORY_SECTION7: "世界は平和を取り戻し、ヒーローは人々から称賛されます。ヒーローは経験を通じて成長し、新たな決意を持って日常生活に戻ります。ヒーローの成長と、彼らが世界に与えた影響を描写し、物語を締めくくってください。"
}
superhero_prompts = {
STORY_SECTION1: "Describe the protagonist's (hero's) daily life and their special abilities or sense of mission. The hero leads an ordinary life while also working to protect people. Depict the hero's character and the world surrounding them.",
STORY_SECTION2: "A significant threat or enemy presence becomes apparent. The hero struggles with whether to use their abilities to deal with it or prioritize their normal life. Describe the hero's emotional journey leading to their determination to confront the enemy, and the reactions of those around them.",
STORY_SECTION3: "The hero begins to take action to confront the enemy. They utilize their abilities to fight the enemy but simultaneously face personal problems and relationship challenges. Portray the hero's exploits and their internal growth.",
STORY_SECTION4: "The hero achieves a significant victory in the battle against the enemy, but at the same time, new threats or problems come to light. The hero gains new recognition of their abilities and role. Describe the turning point in the story and the change in the hero's state of mind.",
STORY_SECTION5: "The enemy demonstrates overwhelming power, and the hero finds themselves in a critical situation. The hero feels the limitations of their abilities and becomes anxious about whether they can fulfill their mission. Depict the hero's lowest point and their search for a way to recover.",
STORY_SECTION6: "The hero gains new powers or insights and faces the final confrontation with the enemy. With the help of their abilities and allies, the hero defeats the enemy. Describe the hero's exploits in the climax and the moment of the enemy's defeat.",
STORY_SECTION7: "The world regains peace, and the hero is praised by the people. The hero grows through their experiences and returns to daily life with new determination. Portray the hero's growth, the impact they had on the world, and conclude the story."
}

genre_name_to_prompt = {
"Monster in the house":"",
"Golden Fleece": "",
"Out of the Bottle": "",
"Dude with a Problem": "",
"Rites of Passage": "",
"Buddy Love": "",
"Whydunit": "",
"Fool Triumphant": "",
"Institutionalized": "",
"Superhero": ""
}

genre_name_to_cue = {
"Monster in the house": monster_in_the_house_prompts,
"Golden Fleece": golden_fleece_prompts,
"Out of the Bottle": out_of_the_bottle_prompts,
"Dude with a Problem": dude_with_a_problem_prompts,
"Rites of Passage": rites_of_passage_prompts,
"Buddy Love": buddy_love_prompts,
"Whydunit": whydunit_prompts,
"Fool Triumphant": fool_triumphant_prompts,
"Institutionalized": institutionalized_prompts,
"Superhero": superhero_prompts
}

section_duration_in_seconds = {
STORY_SECTION1: 120,
STORY_SECTION2: 60,
STORY_SECTION3: 120,
STORY_SECTION4: 60,
STORY_SECTION5: 120,
STORY_SECTION6: 120,
STORY_SECTION7: 60,
}

section_duration_in_counts = {
STORY_SECTION1: 2,
STORY_SECTION2: 1,
STORY_SECTION3: 3,
STORY_SECTION4: 1,
STORY_SECTION5: 2,
STORY_SECTION6: 3,
STORY_SECTION7: 1,
}

# ジャンルを選択する
def select_genre():
    return random.choice(list(genre_name_to_cue.keys()))

def get_genre_system_prompt(genre_name):
    system_prompt = f"""<story><genre>{genre_name}</genre> 
<instructions> <emotion> - In each story beat, ensure that the protagonist's emotions are moved in either a positive or negative direction. Avoid monotony by preventing the overall story from being consistently sad or consistently happy. </emotion> <pacing> - From the "Midpoint" onward, accelerate the pace of the story. In the "Break into Three, Finale" section, reveal significant information about the protagonist and the antagonist. </pacing> <protagonist> - The protagonist should never be passive. Instead, they should always maintain the initiative, driven by strong desires and motivations. </protagonist> <characters> - Give each character a distinctive feature in either their appearance, manner of speech, or actions to help differentiate them from one another. </characters> <adversaries> - When creating the adversaries, challenges, or mysteries that the protagonist faces, make sure they are slightly beyond what the protagonist believes they can overcome. This will help create a sense of tension and personal growth as the story progresses. Furthermore, the antagonists should be sufficiently villainous to provide a strong contrast to the protagonist and heighten the stakes of the conflict. </adversaries> <balance> - Throughout the story, aim to maintain a balance between the protagonist's abilities and the difficulties they encounter. This will keep the listeners engaged and rooting for the protagonist as they navigate the twists and turns of the plot. </balance> <originality> - While adhering to the conventions of this story type, let's use our imagination to weave an original and captivating tale. We'll incorporate engaging settings, compelling characters, and unexpected plot twists to draw in our listeners and keep them hooked until the very end. </originality> </instructions></story>
"""
    return system_prompt

# ジャンルに応じたカンペ用プロンプトを取得する
def get_story_cue(genre_name, story_section_name, counter, output_num):
    if story_section_name not in section_names:
        return ""
    if output_num == 1:
        ret_text = f"""<current_scene> <context>
<story_structure>
<beat_name>"{story_section_name}"</beat_name>
</story_structure> <focus>
For now, let's begin by focusing on the following key points:
<key_points>{genre_name_to_cue[genre_name][story_section_name]}</key_points> </focus> </context>
</current_scene>"""
    else:
        ret_text = f"""<current_scene> <context>
<story_structure>
<beat_name>"{story_section_name}"</beat_name>
<beat_progress_indicator>{counter+1}/{output_num}</beat_progress_indicator>
</story_structure> <focus>
Here are the key points to address in this section: 
<key_points>{genre_name_to_cue[genre_name][story_section_name]}</key_points></focus> </context>
</current_scene>"""
    return ret_text