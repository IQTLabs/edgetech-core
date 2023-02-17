## How to Contribute

1. Fork the Project
2. Create your Feature Branch (`git checkout -b dev`)
3. Commit your Changes (`git commit -m 'adding some feature'`)
4. Run (and make sure they pass):
```
black --diff --check *.py

pylint --disable=all --enable=unused-import *.py

mypy --allow-untyped-decorators --ignore-missing-imports --no-warn-return-any --strict --allow-subclassing-any *.py
```
If you do not have them installed, you can install them with `pip install "black<23" pylint==v3.0.0a3 mypy==v0.991`.

5. Push to the Branch (`git push origin dev`)
6. Open a Pull Request

---

## A Few Stylistic Things to Note

**These are in an attempt to enforce conformity of all future commits. Please suggest via Pull Request any that should be added/amended.**

All of the functionality should be encapsulated in the `*_pub_sub.py` file that sits in the `module/` diretory (in this case `core`). Within this file, a single child class of `BaseMQTTPubSub` should be defined the encapsulates all of the functionality. 

All MQTT client setup and connection should be done using `BaseMQTTPubSub` functionality. If a feature does not exist, please suggest it in that [repository](https://github.com/IQTLabs/edgetech-core). 

All class attributes should be passed as enviornment variables through the `docker-compose.yml` file via the `.env` file. 

Typing should be included in all cases. Running `mypy` before pushing should enforce this and you will not be allowed to merge until the code checks have passed. 

All functions should include docstring comments that generally follow the Google docstring format. 

All functions not meant to be called outside of a class should be denoted with a `_` before the fuction name. In almost every case, each pubsub should only include one `main()` function meant to be called that encapsulates keeping the main thread alive and sets up the relevant services. The majority of the "work" in a module should be done via callbacks.

All unused parameters should be denoted with a `_` in front of them as well. 

Only specified exceptions should be handled. 

Each pubsub module should pubish a registration in the constructor and a heartbeat.

All recurring tasks that need to happen after an interval of time has elapsed should be done so via the [`schedule`](https://schedule.readthedocs.io/en/stable/) library. 

All python dependencies other than `poetry` (which is installed via `pip3`) should be installed using [`poetry`](https://python-poetry.org/). All dependencies should be encapsulated in the `Dockerfile`.