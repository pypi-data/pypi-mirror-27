class LengthTest(object):
    def __init__(self, lang):
        self.name = "Grosse suppression"
        self.lang = lang

        self.fail_marker = emoji("/images/emoji/apple/rage.png?v=3", self.name)
        self.success_marker = ""

    def __call__(self, old_version, new_version):
        old_doc = old_version.document if old_version else None
        new_doc = new_version.document if new_version else None

        if not old_doc or "redirects_to" in old_doc:
            return True, True

        if not new_doc or "redirects_to" in new_doc:
            return True, True

        result = True

        old_locale_length = old_doc.get_locale(self.lang).get_length()
        new_locale_length = new_doc.get_locale(self.lang).get_length()

        if old_locale_length != 0 and new_locale_length / old_locale_length < 0.5:
            result = False

        return True, result


class ReTest(object):
    def __init__(self, name, lang):
        self.name = name
        self.lang = lang
        self.patterns = []
        self.fail_marker = emoji("/images/emoji/apple/red_circle.png?v=3", self.name)
        self.success_marker = emoji("/images/emoji/apple/white_check_mark.png?v=3",
                                    self.name + " corrigé")

    def __call__(self, old_version, new_version):
        old_doc = old_version.document if old_version else None
        new_doc = new_version.document if new_version else None

        def test(doc):
            if not doc or "redirects_to" in doc:
                return True

            return not doc.search(self.patterns, self.lang)

        return test(old_doc), test(new_doc)


class HistoryTest(object):
    activities_with_history = ["snow_ice_mixed", "mountain_climbing", "rock_climbing", "ice_climbing"]

    def __init__(self, lang):
        self.name = "Champ historique"
        self.lang = lang
        self.fail_marker = emoji("/images/emoji/apple/closed_book.png?v=3", self.name)
        self.success_marker = emoji("/images/emoji/apple/green_book.png?v=3", self.name + " rempli")

    def __call__(self, old_version, new_version):
        old_doc = old_version.document if old_version else None
        new_doc = new_version.document if new_version else None

        def test(doc):
            if not doc or "redirects_to" in doc or doc.type != "r":
                return True

            if len([act for act in doc.activities if act in self.activities_with_history]) == 0:
                return True

            locale = doc.get_locale(self.lang)
            if locale and (not locale.route_history or len(locale.route_history) == 0):
                return False

            return True

        return test(old_doc), test(new_doc)


def emoji(src, text):
    return '<img src="{}" class="emoji" title="{}" alt="{}">'.format(src, text, text)


def get_re_tests(configuration, lang):
    result = []

    test = None
    for line in configuration.raw.split("\n"):
        if line.startswith("#"):
            test = ReTest(line.lstrip("# "), lang)
            result.append(test)
        elif line.startswith("    ") and test:
            pattern = line[4:]
            if len(pattern.strip()) != 0:
                test.patterns.append(line[4:])

    return filter(lambda t: len(t.patterns) != 0, result)
