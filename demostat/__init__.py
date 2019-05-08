def __to_version(release):
    v = release.split("-")
    return v[0]

def __is_develop(release):
    return release.endswith("-dev")

name = "demostat"
release = "0.2.4"
version = __to_version(release)
develop = __is_develop(release)
