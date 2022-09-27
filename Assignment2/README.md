# Hometask

### English programming language.

Implement English-to-Clips programming language translator.
Create syntactic constructions, which are similar to correct English speech and are
equivalent to defrule, deftemplate and assert.

E.g.:

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

### Run programm

```shell
$ python3 main.py
```

### Run programm with Docker

```shell
$ docker build -t english-to-clips .
$ docker run -it english-to-clips
```