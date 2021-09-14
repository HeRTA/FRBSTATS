<p align="center">
  <img src="https://i.imgur.com/46QBLvD.png?raw=true" alt="FRBSTATS"/>
</p>

## FRBSTATS: A web-based platform for visualization of fast radio burst properties

<p align="center">
  <a href="https://ascl.net/2106.028"><img src="https://img.shields.io/badge/ascl-2106.028-blue.svg?colorB=262255" alt="ascl:2106.028" /></a>
  <img src="https://img.shields.io/badge/python-3.x-green"/>
  <img src="http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat"/>
  <img src="https://img.shields.io/github/license/HeRTA/FRBSTATS?color=yellow"/>
</p>

**[FRBSTATS](https://www.herta-experiment.org/frbstats)** is a user-friendly web interface that includes an open-access catalogue of FRBs published up to date, along with a highly accurate statistical overview of the observed events.

The platform supports the retrieval of fundamental FRB data either directly through the [FRBSTATS API](https://www.herta-experiment.org/frbstats/api), or in the form of a CSV/JSON-parsed database, while enabling the plotting of parameter distributions for a variety of visualizations. These features allow researchers to conduct more thorough population studies, while narrowing down the list of astrophysical models describing the origins and emission mechanisms behind these sources ([Platts et al., 2019](https://arxiv.org/abs/1810.05836)).

Lastly, the platform provides a visualization tool that illustrates associations between primary bursts and repeaters, complementing basic repeater information provided by the [Transient Name Server (TNS)](https://www.wis-tns.org).

FRBSTATS is a fully **open-source** platform. Anyone is welcome to [contribute](https://github.com/HeRTA/FRBSTATS/issues) with code, data and ideas for improvement.

---
### Citing FRBSTATS

If the FRBSTATS platform contributes to work that leads to publication, please acknowledge the project by **[citing it](https://ascl.net/2106.028)**.

---


### Statement of need

FRB population studies deem the importance of having a reliable & up-to-date database containing fundamental information about all FRB events discovered to date.

The first effort to catalogue FRBs began with [FRBCAT](http://frbcat.org) ([Petroff et al., 2016](http://adsabs.harvard.edu/abs/2016PASA...33...45P)).
Since July 2020 however, FRBCAT has been deprecated. Although all events (up to date) are now submitted
to the TNS, the platform appears to have a lot of
issues that limit FRB population studies:

1. **Data completeness:** Many FRB events listed on the TNS catalogue lack fundamental properties (e.g. for many events, the flux density is either missing, or contains a `0`, which can confuse automation software that obtain TNS data for statistical analysis and yield inaccurate results).

2. **Unit errors:** Events with incorrect units (e.g. mJy listed instead of Jy) have been observed.

3. **Reliability:** There is little to no data traceability that permits the verification of event parameters, and Discovery Reports pages are broken.

4. **Accessibility:** TNS is great for optical transients like supernovae, but navigating through the data of the FRB catalogue is not very convenient, as the user is exposed to columns that are not as relevant to FRBs as they are to optical transients (e.g. `Class`, `Discovery Data Source/s` (identical to `Reporting Group/s`), `Disc. Internal Name` (no clear meaning, possible deprecated designation), `Public` (all events are set to `Y`), `Discovery Filter`, `Sender` (too similar to `Reporting Group/s` to matter to most users)), and not exposed to columns that are more meaningful (e.g. `Width`, `Fluence`, `Center frequency`, `S:N`).

5. **Maintenance:** The TNS group has been notified of some of these problems through their [contact page](https://www.wis-tns.org/content/contact-us), but unfortunately no response has been received. This creates various accessibility issues regarding corrections, modifications and additions to the catalogue by the community (whereas, FRBSTATS enables direct modifications by the community with a simple pull request or issue).

In contrast, FRBSTATS aims to tackle all of these barriers, by researching and manually verifying the parameters of
(hopefully all) FRB events, and providing a decentralized platform for anyone to access, modify and make corrections
to the listed data directly.

On top of serving an open-access catalogue, the FRBSTATS platform provides fundamental statistics about
the FRBs discovered up to date, such as:

- The total observed events as a function of time (MJD);
- Repeaters vs one-off events;
- Galactic sources and
- Event coverage (%).

Additionally, the platform enables astronomers and researchers to rapidly plot parameter distributions for a
variety of visualizations, concerning FRB population studies and more, without having to download and install any
packages on their machine locally. All parametric plots are displayed on the web, as all computations are carried out
by the server automatically.

---

#### Data contribution guidelines (checklist)

1. Append row with new FRB to the [FRBSTATS spreadsheet](https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/edit?usp=sharing).
- Useful conversion tools:
- - UTC ⇄ MJD: https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/xTime/xTime.pl
- - RA/Dec. ⇄ l, b: http://www.astrouw.edu.pl/~jskowron/ra-dec/
3. Export to CSV and commit/submit PR/modify the [`catalogue.csv`](https://github.com/HeRTA/FRBSTATS/blob/main/catalogue.csv) file **(ensure there is no newline at the end of file)**.
4. If new telescope (its first FRB): Append to dictionary [`plot_repeaters.py`](https://github.com/HeRTA/FRBSTATS/blob/main/figs/repeaters/plot_repeaters.py#L99).
5. If galactic source: Add +1 to galactic sources ([`index.html`](https://github.com/HeRTA/FRBSTATS/blob/main/index.html#L182)).
6. If repeater child: Add to [`repeaters.json`](https://github.com/HeRTA/FRBSTATS/blob/main/repeaters.json).
7. Rerun `gitpull.php` with plot batch.
8. Check changes/basic overall functional test.
