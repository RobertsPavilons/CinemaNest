Izmantotās valodas: Python, JavaScript, Html un CSS
Izmantoju Fastapi un SQL Alchemy
Mājaslapas info: Visiem, kuri ir reģistrējušies, ir pieejama MovieNest mājaslapa. Ir diva veida useri- parastie users un admini. Tie, kuri nav reģistrējušies, nevarēs piekļūt nevienam endpointam izņemot / , /register un /login.
Tie, kuri ir useri var skatīt filmas, seriālus, animācijas filmas, izvēlēties random filmu seriālu vai animācijas filmu, kā arī skatīt aktierus. Ir iespēja arī nomainīt savu profila bildi un lietotāja datus. Sarakstos, kur ir redzamas filmas,seriāli un animācijas filmas,
tikai adminiem ir pieejamas un redzamas arī pogas add un konkrēto filmu lapās: /movielist{id} vai /tvshowlist{id} vai /animationmovielist{id} arī pogas edit un delete ir pieejamas tikai adminiem. Mājaslapā izmanto access un jwt tokenus. Lai gan backendā ir definēts
arī refresh token un /refresh, tie frontend netiek izmantoti, jo mājaslapa vēl nav pietiekami liela un pagaidām netiek hostēta,tāpēc pašlaik ir tikai jwt tokens, kurš ir aktīvs 30 minūtes. Mājaslapa pagaidām ir pieejama lokāli.
**Instalācija:**
Ieteicams ielādēt gitbash, bet ja nevēlies, vari izmantot cmd. Gitbash download links: https://git-scm.com/downloads/win
1. Lejupielādē šo github saiti kā zip failu un extracto folderi kaut kur uz desktop.
2. Lejupielādē savā datorā Python https://www.python.org/downloads/
3. Kad python ir instalēts, iegaumē tā atrašanās vietu, kur tas tika nolādēts, parasti tas ir $appdata% un vajadzētu izskatīties šādai lokācijai: C:\Users\...\AppData\Local\Programs\Python\Python313.
4. Šis solis jādara tikai, ja nestrādā 5,6,7,8,9: Atver environment variables, uzspied uz environment variables(var būt atkarīgs no valodas) un apakšā atlasi path, tad nospied edit. Tev atvērsies logs, ar dažādiem pathiem. Tagad noliec šo "gulēt" un ej uz python mapi, kuru jau minēju iepriekš(atkarīgs, kur tu to ieinstallēji): C:\Users\...\AppData\Local\Programs\Python\Python313. Nokopē šī faila lokācijas linku un ej atpakaļ uz environment variables logu, uzspied new un ielīmē python lokācijas linku. Tagad ej atpakaļ uz python mapi, iej scripts, izskatīsies šādi: C:\Users\...\AppData\Local\Programs\Python\Python313\Scripts un arī šo lokāciju nokopē un pievieno vēl vienu environment variable un kad abi pievienoti( gan python 313, gan python313\Scripts) spied Ok un tad vēlreiz Ok. Ja problēmas ar saprašanu var rakstīt discordā RobertsP, vai izmantot youtube tutorial: https://www.youtube.com/watch?v=dj5oOPaeIqI (Sākas ap 2:40) 
5. Atver vai nu gitbash vai cmd. Ja izmanto cmd, tad atlasi mājaslapas folder lokāciju izmantojot "cd". Lūk piemērs: ``cd C:\Users\...\OneDrive\Desktop\MyMovieApp`` Ja izmanto git bash, tad vienkārši ieej mapē, kur atrodas mājaslapa un visi tās kodi un faili un kaut kur,
kur tukšums mapē uzspied labo peles klikšķi un "open gitbash here". Tad vai nu caur gitbash, vai nu ar cmd pamēģini palaist:
6. ``pip install fastapi uvicorn sqlalchemy databases pydantic bcrypt python-multipart jinja2``
Kad šie ieinstalējas, tad runo pip vēlreiz un instalē šos atsevišķi:
7. ``pip install passlib[bcrypt]``
8. ``pip install dotenv``
9. ``pip install python-jose``
10. ``pip install pysqlite3``
11. Ja tomēr kaut kas nav instalējies, vai neiet, ieteicams skatīties, ko saka cmd(ja saka,piemēram, module not found, tad ar pip jāinstalē to moduli, kurš apakšā rādās- tā nosaukumu var atrast internetā.) Ja tomēr kaut kas neiet, rakstiet dm's discordā RobertsP
Kad viss ir instalēts, raksti ``uvicorn main:app --reload`` un tev atvērsies mājaslapa. Ej uz / endpointu un no turienes sāc darbību. Lai forša filmu meklēšana!
**Ja vēlies pamēģināt tikai adminiem speciālos endpointus:**
1. Nolādē sqlite, ja vēl nav: https://www.sqlite.org/download.html. Augšējo: 
``sqlite-src-3490100.zip``
(13.71 MiB) 		Complete canonical source tree for SQLite version 3.49.1, include test cases and extensions. This is a snapshot of all code under version control at the time of release. This is the urtext. All of the other source code bundles shown below are derived from this one.
Un sqlite tools, lūk šos: 
``sqlite-dll-win-x64-3490100.zip``
(1.28 MiB) 		64-bit DLL (x64) for SQLite version 3.49.1.
(SHA3-256: ec8fb7976d9c4bc495c4a142da05e97c4d6dc6c1205877adcce0bd5b191026e2)
``sqlite-tools-win-x64-3490100.zip``
(6.12 MiB) 		A bundle of command-line tools for managing SQLite database files, including (1) the command-line shell, (2) sqldiff.exe, (3) sqlite3_analyzer.exe, and (4) sqlite3_rsync.exe. 64-bit.
2. Visu ielādē un extracto tikai ``sqlite-tools-win-x64-3490100`` zip failu jebkur, kur vēlies. Tu iegūsi parastu folderi, atver to un nokopē lokācijas linku tāpat kā to darīji 4. solī.
3. Šis solis jāievēro tikai, ja ``sqlite3 --version`` neiet: Tāpāt kā 4. solī nokopē lokācijas linku, šoreiz tās mapes linku, kuru extractoji, vajadzētu izskatīties šādi: 
C:\Users\...\Downloads\sqlite-tools-win-x64-3490100(lokācija var atšķirties) un tāpāt ka python, ievieto šo lokāciju environment variables, spiežot path->edit->new->ielīmē->ok->ok. Un tad vai nu gitbash, vai cmd(ar cd atlasot mana koda mapi) palaid ``sqlite3 --version``, ja viss kārtībā, tad uzraksti ``sqlite3 database.db`` un tu varēsi izmantot sqlite komandas.
Lai iedotu sev admin:
Izmanto komandu: ``UPDATE users SET role = 'admin' WHERE username  = 'TavsVards';``
Ja kaut kas nesanāk, raksti discord.
