import en_core_web_sm
from nltk import Tree
from spacy import displacy


class NLP:
    """
        - [ ] deftemplate   :

        ```
        Cat template has properties of color, age, and name.
        (deftemplate cat
            (slot color) (slot age) (slot name))
        ```

        - [ ] defrule:

        ```
        If there exists cat named Bob then there exists a cat named Tom.
        (defrule rule1
            (cat (name “Bob”)) => (assert (cat (name “Tom”))))
        ```

        - [ ] assert:
        ```
        There exists a cat with the name Bob.
        (assert (cat (name “Bob”)))
        ```
    """

    def __init__(self, nlp_loader=en_core_web_sm):
        self.all_dict = None
        self._nlp = nlp_loader.load()
        self.command_keywords = {
            "template": ["template", "struct", "definition", "property", "define"],
            "rule": ["if"],
            "assert": ["assert", "exist"]
        }

        self.command_root_keywords = {"template": ["have"], "rule": ["if"], "assert": ["be"]}

    def nlp(self, inp):
        return self._nlp(inp)

    def teach_me(self):

        new_key = input(f" >> Enter the new key that you used for the previous command\n\t"
                        f"Most probably one from {self.all_dict['subjects']}\n >> Enter: ")
        while True:
            command = input(">> Input the command: ").lower()
            if command in self.command_keywords.keys():
                self.command_keywords[command].append(new_key)
                break

            if command == "exit":
                print("Did not learn new thing :(")
                return

            print("Enter the command from the list (template, rule, assert)")
        print(f"Now, the command {command} has a new keyword: {new_key}")

    def search(self, root):
        for command_key in self.command_keywords.keys():
            for command in self.command_keywords[command_key]:
                if command in self.all_dict["lemma_dict"].keys():
                    if command_key == "template":
                        return self.clips_template(command)

                    if command_key == "rule":
                        return self.clips_rule()

                    if command_key == "assert":
                        return self.clips_assert()

        # Check the root
        for command_key in self.command_root_keywords.keys():
            for command in self.command_root_keywords[command_key]:
                if command == root.lemma_:
                    if command_key == "template":
                        return self.clips_template(command)

                    if command_key == "rule":
                        return self.clips_rule()

                    if command_key == "assert":
                        return self.clips_assert()
        return -1

    def _get_attributes(self):
        # For now only get all the pos_: [pobjs, conj, dobj]
        attributes = []
        for token_text in self.all_dict["tokens_dict"].keys():
            if (self.all_dict["tokens_dict"][token_text].dep_ in ["pobjs", "conj", "dobj"] and
                    self.all_dict["tokens_dict"][token_text].pos_ in ["NOUN"]):
                attributes.append(token_text)

        return attributes

    def _get_template_name(self, command):
        template_name = self.all_dict["tokens_dict"][list(self.all_dict["tokens_dict"].keys())[0]]

        # Iterate all over the tokens to find the template name that is attached to the keyword for template command
        # and at the same time is noun Return the last word that conforms with these conditions

        for token_text in self.all_dict["tokens_dict"].keys():
            if (self.all_dict["tokens_dict"][token_text].pos_ == "NOUN" and self.all_dict["tokens_dict"][
                token_text].dep_ in ["compound", "ROOT", "nsubj"] or (
                    self.all_dict["tokens_dict"][token_text].pos_ == "PROPN" and
                    self.all_dict["tokens_dict"][token_text].dep_ in ["compound"])):
                template_name = token_text
                break

        return template_name

    def clips_template(self, command):
        template_name = self._get_template_name(command)
        attributes = self._get_attributes()
        clips_attributes = [f"(slot {a})" for a in attributes]
        clips = f"(deftemplate {template_name}\n\t{' '.join(clips_attributes)})"
        return clips

    def _get_rule_objs(self):
        obj1 = None
        key_vals1 = {}
        obj2 = None
        key_vals2 = {}
        for token in self.all_dict["doc"]:
            if (token.dep_ in ["dobj", "attr", "nsubj"] and token.pos_ in ["NOUN", "PROPN"] and
                    self.all_dict["tokens_dict"][token.head.text].lemma_ in ["exist", "be"]):
                if obj1 is None:
                    obj1 = token.text
                    continue

                obj2 = token.text
                continue

            if obj1 is not None:
                if obj2 is None:
                    if token.dep_ in ["acl", "amod"] and token.head.text == obj1:
                        value = None
                        for token_ in self.all_dict["doc"]:
                            if token_.head.text == token.text:
                                value = token_.text
                                break

                        key_vals1[token.lemma_] = value

                    elif token.dep_ in ["pobj"] and token.head.text in ["with"]:
                        value = None
                        for token_ in self.all_dict["doc"]:
                            if token_.text == token.text:
                                value = token_.text
                            elif value is not None:
                                break
                        key_vals1[token.lemma_] = value

                    elif token.dep_ in ["acomp"] and self.all_dict["tokens_dict"][token.head.text].lemma_ in ["be"]:
                        key_vals1[token.head.text] = token.text

                else:
                    if token.dep_ in ["acl", "amod"] and token.head.text == obj2:
                        value = None
                        for token_ in self.all_dict["doc"]:
                            if token_.head.text == token.text:
                                value = token_.text
                        key_vals2[token.lemma_] = value

                    elif token.dep_ in ["pobj"] and token.head.text in ["with"]:
                        value = None
                        for token_ in self.all_dict["doc"]:
                            if token_.head.text == token.text:
                                value = token_.text
                            elif value is not None:
                                value = token_.text
                                break
                        key_vals2[token.lemma_] = value

                    elif token.dep_ in ["acomp"] and self.all_dict["tokens_dict"][token.head.text].lemma_ in ["be"]:
                        key_vals2[token.head.text] = token.text

        return obj1, key_vals1, obj2, key_vals2

    def clips_rule(self):
        obj1, key_vals1, obj2, key_vals2 = self._get_rule_objs()
        key_vals1_compound = [f'({k} "{v}")' for k, v in key_vals1.items()]
        key_vals2_compound = [f'({k} "{v}")' for k, v in key_vals2.items()]
        clips = f"(defrule rule1 \n({obj1} {' '.join(key_vals1_compound)}) => (assert ({obj2} {' '.join(key_vals2_compound)}))) "
        return clips

    def _get_asserted_obj(self):
        obj = None
        for token_text in self.all_dict["tokens_dict"].keys():
            if ((self.all_dict["tokens_dict"][token_text].dep_ in ["nsubj", "attr"] and \
                 self.all_dict["tokens_dict"][token_text].head.text in self.all_dict["lemma_dict"]["be"]) or \
                    self.all_dict["tokens_dict"][token_text].dep_ in ["ROOT"]):
                obj = token_text

        return obj

    def _get_assertion_keys_values(self):
        # keys are pobj and head.text="with"
        assertions_dict = {}
        for token_text in self.all_dict["tokens_dict"].keys():
            if (self.all_dict["tokens_dict"][token_text].dep_ in ["pobj"] and \
                    self.all_dict["tokens_dict"][token_text].head.text in ["with"]):
                value = None
                for token in self.all_dict["doc"]:
                    if token.head.text == token_text:
                        value = token.text

                assertions_dict[token_text] = value
        return assertions_dict

    def clips_assert(self):
        asserted_obj = self._get_asserted_obj()
        key_vals = self._get_assertion_keys_values()
        clips_attributes = [f'({k} "{v}")' for k, v in key_vals.items()]
        clips = f"(assert {asserted_obj} {' '.join(clips_attributes)})"
        return clips

    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node.orth_, [self.to_nltk_tree(child) for child in node.children])
        else:
            return node.orth_

    def process(self, user_input, render=False):
        self.all_dict = {"subjects": {},  # dictionaries: keys are the text and the value is the token itself
                         "actions": {},
                         "objects": {},
                         "tokens_dict": {},
                         "lemma_dict": {},  # Here: key is the lemma and the value is the text
                         "doc": None
                         }

        doc = self.nlp(user_input)
        self.all_dict["doc"] = doc

        # Store the subjs, acts, objs, and all the tokens in dictionaries
        for token in doc:
            token_text = token.text.lower()
            role = token.dep_
            if role == "nsubj":
                self.all_dict["subjects"][token_text] = token
            if role == "ROOT":
                self.all_dict["actions"][token_text] = token
            if role == "dobj":
                self.all_dict["objects"][token_text] = token

            self.all_dict["tokens_dict"][token_text] = token

            if token.lemma_ in self.all_dict["lemma_dict"]:
                self.all_dict["lemma_dict"][token.lemma_].append(token.text)
            else:
                self.all_dict["lemma_dict"][token.lemma_] = [token.text]

        # Visualization
        if render:
            for token in doc:
                print("Word = {}, Lemma = {}, PoS/Tag = {}/{}, Role = {} to [{}]".format(
                    token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.text))

            print("Display")
            displacy.render(doc, jupyter=True, style='dep')
            self.to_nltk_tree(list(doc.sents)[0].root).pretty_print()

            [self.to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

        # Search for the keywords for the commands
        search_result = self.search(list(doc.sents)[0].root)
        if search_result is not None:
            return search_result
        self.teach_me()
        return -1
