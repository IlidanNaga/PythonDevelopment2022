import cmd
import pynames
import shlex

import importlib
import inspect

from pkgutil import iter_modules

class Generator(cmd.Cmd):
    
    generators = {}

    for submodule in iter_modules(pynames.generators.__path__):
        
        mod = submodule.name
        generators[mod] = None
        
        full_name = "pynames.generators." + mod
        module = importlib.import_module(full_name)
        subnames = []
        
        for name, obj in inspect.getmembers(module):
            
            if inspect.isclass(obj) and obj.__module__ == full_name:
                form = name.lower().replace('fullname', '').replace('names', '').replace('generator', '')
                subnames.append((form, obj))
                
        if subnames.__len__() > 1:
            
            sub = {}
            for a, b in subnames:
                sub[a] = b()
            generators[mod] = sub
            
        else:
            generators[mod] = subnames[0][1]()


    def __init__(self, *args, **kwargs):
        super(Generator, self).__init__(*args, **kwargs)
        self.lang = pynames.LANGUAGE.NATIVE
        self.prompt = ' >  '

        self.nations = list(Generator.generators.keys())

    def get_prefixes(self, names, prefix):
        return [name for name in names if name.startswith(prefix)]
        
    def do_generate(self, phrase):
        
        """
        Generation and display of a name
        Format: generate class [subclass] [gender]
        """
    
        args = shlex.split(phrase)
        
        if not len(args) or args[0].lower() not in Generator.generators:
            return
        
        # existance of a subclass:
        if type(Generator.generators[args[0].lower()]) == dict:
            
            if len(args) > 1 and args[1].lower() in Generator.generators[args[0].lower()]:
                gen = Generator.generators[args[0].lower()][args[1].lower()]
            else:
                gen = Generator.generators[args[0].lower()][list(Generator.generators[args[0].lower()].keys())[0]]
    
        else:
            gen = Generator.generators[args[0].lower()]
            
        # choice of a gender:
        gender = 'f' if (('female' in args) or ('f' in args)) else 'm'
        
        # checking if selected language is possible. Otherwise - NATIVE would do?
        if self.lang in [*gen.languages]:
            print(gen.get_name_simple(gender, self.lang))

        else:
            print(gen.get_name_simple(gender, pynames.LANGUAGE.NATIVE))


    def complete_generate(self, text, line, begidx, endidx):
        genders = ['male', 'female']

        # finished phrase
        if genders[0] in line.lower() or genders[1] in line.lower():
            return []

        for gen_name in Generator.generators:

            gen = Generator.generators[gen_name]
            
            if gen_name in line.lower():
                
                if type(gen) == dict:

                    for subgen in gen:
                        if subgen in line.lower():
                            return self.get_prefixes(genders, text)

                    return self.get_prefixes(list(gen.keys()), text)

                return self.get_prefixes(genders, text)
        
        return self.get_prefixes(list(Generator.generators.keys()), text)


    def do_language(self, phrase):
        
        """
        Selection of a language ru/en/native
        Format: language ru/en/native
        """
        
        args = shlex.split(phrase)
        
        if len(args):
            self.lang = args[0].lower() if args[0].lower() in pynames.LANGUAGE.ALL else pynames.LANGUAGE.NATIVE
        else:
            self.lang = pynames.LANGUAGE.NATIVE


    def complete_language(self, text, line, begidx, endidx):
        for language in pynames.LANGUAGE.ALL:
            if language in line:
                return []
        return self.get_prefixes(pynames.LANGUAGE.ALL, text)
            
            
    def do_info(self, phrase):
        
        """
        Information of total count of names (with or w/o gender lock) or available langs
        Format: info class [subclass][female|male|language]
        """
        
        args = shlex.split(phrase)
        
        if not len(args) or args[0].lower() not in Generator.generators:
            return
        
        gen = Generator.generators[args[0].lower()]

        if len(args) == 1:

            if type(gen) == dict:
                print(gen[list(gen.keys())[0]].get_names_number())
            else:
                print(gen.get_names_number())
            
        else:

            if type(gen) == dict:

                if args[1] in gen:
                    gen = gen[args[1]]
                    
                    if len(args) > 2:
                        args[1] = args[2]

                    else:
                        print(gen.get_names_number())
                else:
                    gen = gen[list(gen.keys())[0]]

            if args[1][0].lower() in ['f', 'm']:
                print(gen.get_names_number(args[1][0].lower()))
                
            elif args[1].lower() == 'language':

                print(*gen.languages)

    
    def complete_info(self, text, line, begidx, endidx):
        terminal = ['male', 'female', 'language']

        args = shlex.split(line.lower())

        if (set(terminal) & set(args)).__len__() > 0:
            return []

        for gen_name in Generator.generators:

            gen = Generator.generators[gen_name]

            if gen_name in line.lower():

                if type(gen) == dict:

                    for subgen_name in gen.keys():

                        if subgen_name in line.lower():
                            return self.get_prefixes(terminal, text)

                    return self.get_prefixes(list(gen.keys()), text)
                return self.get_prefixes(terminal, text)

        return self.get_prefixes(list(Generator.generators.keys()), text)

    
    def do_exit(self, phrase):
        
        """
        Exit the interpreter
        Format: exit
        """
        return True


if __name__ == "__main__":
    Generator().cmdloop()