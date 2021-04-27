<p align="center">
  <img src="https://i.imgur.com/46QBLvD.png?raw=true" alt="FRBSTATS"/>
</p>

## FRBSTATS: A web-based platform for visualization of fast radio burst properties

**[FRBSTATS](https://www.herta-experiment.org/frbstats)** is a user-friendly web interface that includes an open-access catalogue of FRBs published up to date, along with a highly accurate statistical overview of the observed events.

The platform supports the retrieval of fundamental FRB data either directly through the [FRBSTATS API](https://www.herta-experiment.org/frbstats/api), or in the form of a CSV/JSON-parsed database, while enabling the plotting of parameter distributions for a variety of visualizations. These features allow researchers to conduct more thorough population studies, while narrowing down the list of astrophysical models describing the origins and emission mechanisms behind these sources ([Platts et al., 2019](https://arxiv.org/abs/1810.05836)).

Lastly, the platform provides a visualization tool that illustrates associations between primary bursts and repeaters, complementing basic repeater information provided by the [Transient Name Server (TNS)](https://www.wis-tns.org).

FRBSTATS is a fully **open-source** platform. Anyone is welcome to [contribute](https://github.com/HeRTA/FRBSTATS/issues) with code, data and ideas for improvement.

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

5. **Maintenance:** The TNS group has been notified of some of these problems through their [contact page](https://www.wis-tns.org/content/contact-us), but no response has been received. It is therefore inaccessible for one to make corrections of the catalogue.

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
