# Contributor guidelines

The following guide is directed to contributors wishing to enrich the current **FRBSTATS** database.

### About the platform

Accessible via a user-friendly web interface, **FRBSTATS** includes an open-access catalogue of Fast
Radio Bursts (FRBs) published up to date, along with a statistical overview of the observed events.
In addition to the ability of obtaining FRB data directly through the FRBSTATS API, the platform
supports the plotting of parameter distributions for a variety of visualizations.

### Statement of need

Fast radio bursts currently consist one of the most important topics in astronomy. With only 290 events
observed to date, any information derived from the few successful detections is of high value, and can
assist researchers in narrowing down the list of astrophysical models describing the emission mechanisms
and the origins of these sources ([Platts et al., 2019](https://arxiv.org/abs/1810.05836)). It is
therefore important to have a reliable database containing fundamental information about all FRBs.

The first effort to catalogue FRBs began with [FRBCAT](http://frbcat.org/) ([Petroff et al., 2016](http://adsabs.harvard.edu/abs/2016PASA...33...45P)).
Since July 2020 however, FRBCAT has been deprecated. Although all events (up to date) are now submitted
to the [Transient Name Server (TNS)](https://www.wis-tns.org/), the platform appears to have a lot of
issues that limit FRB population studies:

1. **Data completeness:** Many FRB events listed on the TNS catalogue lack fundamental properties (e.g. for many events, the flux density is either missing, or contains a `0`, which can confuse automation software that obtain TNS data for statistical analysis and yield inaccurate results).

2. **Unit errors:** Events with incorrect units (e.g. mJy listed instead of Jy) have been observed.

3. **Reliability:** There is little to no data traceability that permits the verification of event parameters, and Discovery Reports pages are broken.

4. **Accessibility:** TNS is great for optical transients like supernovae, but navigating through the data of the FRB catalogue is not very convenient, as the user is exposed to columns that are not as relevant to FRBs as they are to optical transients (e.g. `Class`, `Discovery Data Source/s` (identical to `Reporting Group/s`), `Disc. Internal Name` (no clear meaning, possible deprecated designation), `Public` (all events are set to `Y`), `Discovery Filter`, `Sender` (too similar to `Reporting Group/s` to matter to most users)), and not exposed to columns that are more meaningful (e.g. `Width`, `Fluence`, `Center frequency`, `S:N`)

5. **Maintenance:** The TNS group has been notified of some of these problems through their [contact page](https://www.wis-tns.org/content/contact-us), but no response has been received. It is therefore inaccessible for one to make corrections of the catalogue.

In contrast, FRBSTATS aims to tackle all of these barriers, by researching and manually verifying the parameters of
(hopefully all) FRB events, and providing a decentralized platform for anyone to access, modify and make corrections
to the listed data directly.

On top of serving an open-access catalogue, the FRBSTATS platform provides fundamental statistics about
the FRBs discovered up to date, such as:

- Total observed events as a function of MJD;
- Repeaters vs one-off events;
- Galactic sources and
- Verification coverage (%).

Additionally, the platform enables astronomers and researchers to rapidly plot parameter distributions for a
variety of visualizations, concerning FRB population studies and more, without having to download and install any
packages locally on their machine. All parametric plots are displayed on the web, as everything is carried out
by the server automatically.

## Contributing

For the convenience of the contributors, the **FRBSTATS** catalogue has been copied **[here](https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/edit?usp=sharing)**.
This allows everyone to gather information from the TNS into one sheet that everyone can view and modify.

There are **17 columns** for each FRB:

| FRB	| UTC	| MJD	| Telescope	| SEFD | RA | Dec. | l | b | Frequency | DM | Flux | Width | Fluence | S:N | Status | Contributor |
| :-- | :-- | :-- | :-------- | :--- | :-- | :--- | :-- | :-- | :-------- | :- | :--- | :---- | :------ | :-- | :----- | :---------- |

While most of the columns have been derived from TNS automatically with a custom [Python script](https://github.com/HeRTA/FRBSTATS/blob/main/parser.py),
there is still a lot of columns left to be filled that cannot be obtained from TNS in an automated fashion as easily.
These **5 columns** are highlighted in red, and they require the attention of the contributors.

Cells with `x` imply an unknown value (i.e. blank). Note that the `Flux` column has a lot of blanks and `0`s. While
this column has been acquired automatically, many values are incorrect (`0`), or missing (blank). This column can be
ignored for now (since TNS appears to not have such information), and will be revised at a later stage.

### Filling in the data

A link to FRB data can be found [here](https://www.wis-tns.org/search?&discovered_period_value=&discovered_period_units=days&unclassified_at=0&classified_sne=0&include_frb=1&name=frb&name_like=0&isTNS_AT=all&public=all&ra=&decl=&radius=&coords_unit=arcsec&reporting_groupid%5B%5D=null&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=null&at_type%5B%5D=5&date_start%5Bdate%5D=&date_end%5Bdate%5D=&discovery_mag_min=&discovery_mag_max=&internal_name=&discoverer=&classifier=&spectra_count=&redshift_min=&redshift_max=&hostname=&ext_catid=&ra_range_min=&ra_range_max=&decl_range_min=&decl_range_max=&discovery_instrument%5B%5D=null&classification_instrument%5B%5D=null&associated_groups%5B%5D=null&official_discovery=0&official_classification=0&at_rep_remarks=&class_rep_remarks=&frb_repeat=all&frb_repeater_of_objid=&frb_measured_redshift=0&frb_dm_range_min=&frb_dm_range_max=&frb_rm_range_min=&frb_rm_range_max=&frb_snr_range_min=&frb_snr_range_max=&frb_flux_range_min=&frb_flux_range_max=&num_page=500&display%5Bredshift%5D=0&display%5Bhostname%5D=0&display%5Bhost_redshift%5D=0&display%5Bsource_group_name%5D=0&display%5Bclassifying_source_group_name%5D=0&display%5Bdiscovering_instrument_name%5D=0&display%5Bclassifing_instrument_name%5D=0&display%5Bprograms_name%5D=0&display%5Binternal_name%5D=0&display%5BisTNS_AT%5D=0&display%5Bpublic%5D=0&display%5Bend_pop_period%5D=0&display%5Bspectra_count%5D=0&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=0&display%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=0&display%5Bremarks%5D=0&display%5Bsources%5D=0&display%5Bbibcode%5D=0&display%5Bext_catalogs%5D=0&display%5Brepeater_of_objid%5D=0&display%5Bdm%5D=1&display%5Bgalactic_max_dm%5D=0&display%5Bbarycentric_event_time%5D=0&display%5Bpublic_webpage%5D=0) (TNS page).

Information can be found by clicking on the FRB of interest and looking through the `FRB reports` and `Photometry (Burst Properties)` sections.
These will typically include the information you are looking for, but in case you don't see a certain parameter listed,
replace `x` with `?` (`x` is an indicator that the cell has not been checked, so `?` should serve as an indicator to prevent
another contributor from checking the same parameter again).

Once you've filled in the parameters for an FRB, add your name to the last column (`Contributors`) in order
to enable a level of traceability and prevent confusions in case something is unclear and clarifications
are requested.

### Other columns (non-red)

The rest of the columns do not have to be filled in by contributors. Once most of the data is set in place,
a script will automatically transform `UTC` to `MJD`, `RA`/`Dec.` to *`l`*, *`b`*, and `Telescope` to `SEFD`,
eventually completing the catalogue.

