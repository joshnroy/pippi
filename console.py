import cmd
import os
import sys
import math
import dsp
import alsaaudio
import time
import rt
import multiprocessing as mp

class Pippi(cmd.Cmd):
    """ Pippi Console 
    """

    prompt = 'pippi: '
    intro = 'Pippi Console'

    cc = {} 
    vid = 0

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.server = mp.Manager()
        self.voices = self.server.Namespace()

        self.vid = 0

        self.qu = {
                'downbeat': mp.Event(),
                'tick': mp.Event(),
            }

        self.grid = mp.Process(target=rt.grid, args=(self.qu,))
        self.grid.start()

    def play(self, cmd):
        orcs = os.listdir('orc/')
        for orc in orcs:
            if cmd[0] == orc[0:2]:
                gen = cmd[0]
                cmd.pop(0)
                orc = 'orc.' + orc.split('.')[0]
                pl = __import__(orc, globals(), locals(), ['play'])

                for c in self.cc:
                    if c == t or c == 'g':
                        cmd = cmd + self.cc[c]

                # Create a shared list for the voice
                self.vid += 1
                print self.vid, gen, cmd
                voice_id = self.vid

                voice = {'snd': '', 'next': '', 'loop': True, 'regen': False, 'tvol': 1.0, 'cmd': cmd, 'gen': gen}
                setattr(self.voices, str(voice_id), voice)

                process = mp.Process(target=rt.out, args=(pl.play, gen, self.voices, voice_id, self.qu))
                process.start()

                return True

        print 'not found'

    def do_c(self, cmd):
        cmd = cmd.split(' ')
        t = cmd[0]
        cmd.pop(0)
        self.cc[t] = cmd

    def do_ss(self, cmd):
        for vid in range(1, self.vid + 1):
            if hasattr(self.voices, str(vid)):
                voice = getattr(self.voices, str(vid))
                voice['loop'] = False
                setattr(self.voices, str(vid), voice)

    def do_s(self, cmd):
        cmds = cmd.split(' ')

        for cmd in cmds:
            vid = cmd.strip() 
            voice = getattr(self.voices, vid)
            voice['loop'] = False
            setattr(self.voices, vid, voice)

    def do_r(self, cmd):
        cmds = cmd.split(' ')

        for vid in range(1, self.vid + 1):
            if hasattr(self.voices, str(vid)):
                update = False
                voice = getattr(self.voices, str(vid))

                # loop through cmds and split
                for cmd in cmds:
                    cmd = cmd.split(':')
                    for c in voice['cmd']:
                        if cmd[0] == c[len(cmd[0])]:
                            update = True
                            voice['cmd'][i] = cmd[0] + ':' + cmd[1]

                if update is True:
                    voice['cmd'] += ['one']
                    setattr(self.voices, str(vid), voice)
                

    def do_vv(self, cmd):
        cmds = cmd.split(' ')

        for vid in range(1, self.vid + 1):
            self.setvol(vid, cmds[1], cmds[0])

    def do_v(self, cmd):
        cmds = cmd.split(' ')
        self.setvol(cmds[0], cmds[1])

    def setvol(self, vid, vol, gen='a'):
        if hasattr(self.voices, str(vid)):
            voice = getattr(self.voices, str(vid))
            if gen == voice['gen'] or gen == 'a':
                voice['tvol'] = float(vol) / 100.0
                setattr(self.voices, str(vid), voice)

    def do_i(self, cmd=[]):
        for vid in range(1, self.vid + 1):
            if hasattr(self.voices, str(vid)):
                voice = getattr(self.voices, str(vid))
                print vid, voice['gen'], voice['cmd'], 'v:', voice['tvol'], 'l:', voice['loop'], 're:', voice['regen']

    def do_p(self, cmd):
        if cmd == 's1aa':
            cmd = [
                    'dr o:2 n:bb t:40 h:1 wf:sine2pi',
                    'dr o:2 n:eb t:36 h:2 wf:sine2pi',
                    'dr o:2 n:eb t:35 h:1 wf:sine2pi a v:6',
                    'dr o:2 n:eb t:25 h:2 wf:sine2pi a v:6',
                    'sp w:80 m:70 v:40 wf:sine2pi o:2 n:ab re',
                    'sp w:40 m:120 v:50 wf:sine2pi o:2 n:ab re',
                    ]

        elif cmd == 's1ab':
            cmd = [
                    'dr o:2 n:eb.ab t:36 h:1.2.4 v:15 re w wf:sine2pi',
                    'dr o:1 n:eb t:30 h:2.4 wf:tri',
                    'dr o:2 n:bb t:32 h:1.2.4 wf:sine2pi',
                    ]

        elif cmd == 's1ac':
            cmd = [
                    'dr o:4 n:eb t:27 h:1 wf:sine2pi bend re v:1',
                    'dr o:4 n:eb t:20 h:1 wf:sine2pi bend re v:1',
                    ]

        elif cmd == 's1ad':
            cmd = [
                    'dr o:2 n:ab t:27 h:1.2.3.4.5 wf:tri',
                    'dr o:2 n:eb t:23 h:1.2.3.4 wf:tri',
                    ]

        elif cmd == 's1ba':
            cmd = [
                    'dr o:1 t:25 n:ab h:1.2.3.4.5.6 wf:tri',
                    'dr o:1 t:20 n:ab h:1.2.3.4.5.6 wf:tri',
                    'dr o:1 t:16 n:ab h:1 wf:sine2pi',
                    ]

        elif cmd == 's1bb':
            cmd = [
                    'dr o:1 t:6 n:ab h:1.2.3.4.5.6 wf:vary w',
                    'dr o:2 t:9 n:ab h:1.2.3.4.5.6 wf:vary w',
                    'dr o:2 t:7 n:ab h:1.2.3.4.5.6 wf:vary w',
                    'dr o:3 t:3 n:ab h:1.2.3.4.5.6 wf:vary w',
                    'dr o:2 t:10 n:ab h:1.2.3.4.5.6 wf:vary',
                    'dr o:2 t:10 n:ab h:1.2.3.4.5.6 wf:tri',
                    'sh o:2 i:c e:sine re t:2 n:ab s:1',
                    'sh o:2 i:c e:sine re t:1.4 n:ab s:1',
                    ]

        elif cmd == 's2aa':
            cmd = [
                    'sh o:2 n:db s:1 e:phasor qs qu qb:1.3.5.7.9.11.13.15 t:0.06 r:1',
                    'sh o:2 n:db s:5 e:phasor qs qu qb:1.9 t:0.08 r:1',
                    ]

        elif cmd == 's2ab':
            cmd = [
                    'cl w:10 d:h qs qu qb:1.3.5.7.9.11.13.15 b:1',
                    ]

        elif cmd == 's2ac':
            cmd = [
                    'sh o:2 n:db s:8 qs qu qb:1.3.5.7.9.11.13.15 t:0.1 r:1',
                    'sh o:2 n:db s:11 qs qu qb:1.5.9.13 t:0.15 r:1',
                    'cl d:h qu w:10 b:1',
                    ]

        elif cmd == 's2ad':
            cmd = [
                    'sh o:3 n:db s:8 qs qu:16 r:1 t:0.08 e:phasor v:5 i:g',
                    #'sh o:3 n:db s:1.2.5.8 r:3 qu:8 a i:r',
                    #'sh o:3 n:db s:1.2.5.8 r:3 qu:8 a re i:r',
                    #'sh o:2 n:db s:1.2.5.8 r:1 qu:8 a re i:r',
                    #'sh o:2 n:db s:1.2.5.8 r:1 qu:8 a i:r',
                    'cl d:k qs qu b:1 v:150 single re',
                    'cl d:c w:15 qs qu qb:1.5.9.13 b:2 v:8 single re',
                    'cl d:c w:20 qs qu qb:1.3.4.5.7.8.9.11.13.15 b:1 v:5 single',
                    ]

        elif cmd == 's2b':
            cmd = [
                    'sp v:50 w:400 m:10 o:2 wf:tri n:db re',
                    'sp v:30 w:1400 m:15 o:1 wf:tri n:db',
                    'sp v:60 w:50 m:15 o:2 wf:tri n:db re',
                    ]

        elif cmd == 's2c':
            cmd = [
                    'sp n:db w:1 m:40 wf:random re',
                    'sp n:db w:3 o:1 m:50 wf:random re',
                    ]

        elif cmd == 's2d':
            cmd = [
                    'sp n:db w:3 o:2 m:50 wf:random re',
                    'sp n:db w:10 m:55 wf:random re',
                    'sp n:db w:5 m:45 wf:random re',
                    'sp n:db w:20 m:40 o:1 wf:random re',
                    ]

        for c in cmd:
            if len(c) > 2:
                self.default(c)
                dsp.delay(0.1)

    def default(self, cmd):
        cmd = cmd.strip().split(',')
        for c in cmd:
            cc = c.strip().split(' ')
            try:
                getattr(self, 'do_' + cc[0])(c[3:])

            except:
                self.play(cc)


    def do_EOF(self, line):
        return True

    def postloop(self):
        pass

if __name__ == '__main__':
        # Create console
        console = Pippi()

        # Start looping command prompt
        console.cmdloop()
