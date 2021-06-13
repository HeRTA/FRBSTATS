<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Catalogue | FRBSTATS</title>

    <link rel="shortcut icon" href="favicon.ico" />

    <!-- Fonts -->
    <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <script src="script.js"></script>
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

    <!-- Custom styles -->
    <link href="css/style.min.css" rel="stylesheet">

    <!-- Custom styles for page -->
    <link href="vendor/datatables/datatables.bootstrap4.min.css" rel="stylesheet">

</head>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">

        <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href=".">
                <div class="sidebar-brand-icon rotate-n-0">
                    <i class="fas fa-database"></i>
                </div>
                <div style="font-size: 18px;" class="sidebar-brand-text mx-2">FRBSTATS</div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item -->
            <li class="nav-item">
                <a class="nav-link" href=".">
                    <i style="font-size:15px" class="fas fa-fw fa-info-circle"></i>
                    <span style="font-size:15px">Overview</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Nav Item -->
            <li class="nav-item active">
                <a class="nav-link" href="catalogue">
                    <i style="font-size:15px" class="fas fa-fw fa-clipboard-list"></i>
                    <span style="font-size:15px">Catalogue</span></a>
            </li>

             <!-- Nav Item -->
            <li class="nav-item">
                <a class="nav-link" href="repeaters">
                    <i style="font-size:15px" class="fas fa-fw fa-sync-alt"></i>
                    <span style="font-size:15px">Repeaters</span></a>
            </li>

            <!-- Nav Item -->
            <li class="nav-item">
                <a class="nav-link" href="plots">
                    <i style="font-size:15px" class="fas fa-fw fa-chart-line"></i>
                    <span style="font-size:15px">Plots</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item -->
            <li class="nav-item">
                <a class="nav-link" href="api">
                    <i style="font-size:15px" class="fas fa-fw fa-cog"></i>
                    <span style="font-size:15px">API</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider d-none d-md-block">

            <!-- Sidebar Toggler (Sidebar) -->
            <div class="text-center d-none d-md-inline">
                <button class="rounded-circle border-0" id="sidebarToggle"></button>
            </div>

        </ul>
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column" onclick='$("tr:even").css("background-color", "#F2F2F2");$("tr:odd").css("background-color", "#FFFFFF");$("tr:eq(0)").css("background-color", "#ECF3FA");'>

            <!-- Main Content -->
            <div id="content">

                <!-- Topbar -->
                <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

                    <!-- Sidebar Toggle (Topbar) -->
                    <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                        <i class="fa fa-bars"></i>
                    </button>



                    <!-- Topbar Navbar -->
                    <ul class="navbar-nav">

                        <a style="font-size:28px;color:#4e73df">FRBSTATS:</a>
                        <a style="font-size:28px;color:#5a5c69;white-space: pre"> Catalogue</a>


                    </ul>

                </nav>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                    <h1 class="h3 mb-2 text-gray-800">About</h1>
                    <p class="mb-4">This catalogue contains Fast Radio Burst (FRB) events published up to date. Event data have been obtained from the <a target="_blank" href="https://www.wis-tns.org">Transient Name Server (TNS)</a>, <a target="_blank"
                            href="https://www.frbcat.org">FRBCAT</a> (<a target="_blank" href="http://adsabs.harvard.edu/abs/2016PASA...33...45P">Petroff et al., 2016</a>) and the cited publications (see <b>Reference</b> column).</p>

                    <!-- DataTales Example -->
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <div class="d-sm-flex align-items-center justify-content-between mb-4">
                              <abbr style="font-size:22px" class="m-0 font-weight-bold text-primary">FRB Catalogue</abbr>
                                <div class="d-sm-inline-flex align-items-center justify-content-between mb-4">
                                    <a href="catalogue.csv" download class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i
                                        class="fas fa-file-csv text-white-50"></i> Export as <b>CSV</b></a>
                                    <a href="catalogue.json" download class="d-none d-sm-inline-block btn btn-sm btn-info shadow-sm"><i
                                        class="fas fa-brackets-curly text-white-50"></i> Export as <b>JSON</b></a>
                                    <a target="_blank" href="https://docs.google.com/spreadsheets/d/1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY/edit?usp=sharing" class="d-none d-sm-inline-block btn btn-sm btn-success shadow-sm"><i
                                        class="fas fa-file-excel text-white-50"></i> View <b>Spreadsheet</b></a>
                                </div>
                            </div>
                        </div>
                        <div class="card-body">
                          <div>
                          Toggle columns:
                          <a style="font-weight: bold" id="frb" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="0">FRB</a> -
                          <a style="font-weight: normal" id="utc" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="1">UTC</a> -
                          <a style="font-weight: normal" id="mjd" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="2">MJD</a> -
                          <a style="font-weight: bold" id="telescope" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="3">Telescope</a> -
                          <a style="font-weight: bold" id="ra" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="4">RA</a> -
                          <a style="font-weight: bold" id="dec" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="5">Dec.</a> -
                          <a style="font-weight: normal" id="l" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="6">Gal. Long.</a> -
                          <a style="font-weight: normal" id="b" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="7">Gal. Lat.</a> -
                          <a style="font-weight: normal" id="frequency" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="8">Center Frequency</a> -
                          <a style="font-weight: bold" id="dm" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="9">DM</a> -
                          <a style="font-weight: bold" id="flux" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="10">Peak Flux Density</a> -
                          <a style="font-weight: normal" id="width" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="11">Burst Width (FWHM)</a> -
                          <a style="font-weight: normal" id="fluence" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="12">Fluence</a> -
                          <a style="font-weight: normal" id="snr" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="13">S:N</a> -
                          <a style="font-weight: bold" id="verified" onclick="if (document.getElementById(this.id).style.fontWeight == 'normal' || document.getElementById(this.id).style.fontWeight == '') {document.getElementById(this.id).style.fontWeight = 'bold'}else {document.getElementById(this.id).style.fontWeight = 'normal';}" class="toggle-vis" data-column="14">Reference</a>
                        </div>
                            <div style="height:10px;"></div>
                            <div class="table-responsive">
                                <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                                    <thead>
                                        <tr>
                                            <th>FRB</th>
                                            <th>UTC</th>
                                            <th>MJD</th>
                                            <th>Telescope</th>
                                            <th>RA (<i>α</i>)</th>
                                            <th>Dec. (<i>δ</i>)</th>
                                            <th>Gal. Long. (<i>l</i>)</th>
                                            <th>Gal. Lat. (<i>b</i>)</th>
                                            <th>Frequency (MHz)</th>
                                            <th>DM (pc cm⁻³)</th>
                                            <th>Flux (Jy)</th>
                                            <th>Width (ms)</th>
                                            <th>Fluence (Jy ms)</th>
                                            <th>S:N</th>
                                            <th>Reference</th>
                                        </tr>
                                    </thead>
                                    <tbody>

                                    <?php
                                    require "vendor/autoload.php";
                                    $client = new MongoDB\Client(
                                        'mongodb://localhost:27017'
                                    );
                                    $db = $client->frbstats;
                                    $collection = $db->catalogue;
                                    $cursor = $collection->find();
                                    $itr = new IteratorIterator($cursor);
                                    $itr -> rewind();
                                    while ($cursor = $itr->current()){

                                        //echo ;
                                        echo "<tr>";
                                        echo "<td>".$cursor['frb']."</td>";
                                        echo "<td>".$cursor['utc']."</td>";
                                        echo "<td>".$cursor['mjd']."</td>";
                                        echo "<td>".$cursor['telescope']."</td>";
                                        echo "<td>".$cursor['ra']."</td>";
                                        echo "<td>".$cursor['dec']."</td>";
                                        echo "<td>".$cursor['l']."</td>";
                                        echo "<td>".$cursor['b']."</td>";
                                        echo "<td>".$cursor['frequency']."</td>";
                                        echo "<td>".$cursor['dm']."</td>";
                                        echo "<td>".$cursor['flux']."</td>";
                                        echo "<td>".$cursor['width']."</td>";
                                        echo "<td>".$cursor['fluence']."</td>";
                                        echo "<td>".$cursor['snr']."</td>";
                                        echo "<td style='vertical-align: middle;padding-top: 0px;padding-bottom: 0px'><center><a href='".$cursor['ref']."' target='_blank' title='Verified' class='btn btn-secondary btn-circle btn-sm'><i class='fas fa-scroll'></i></a></center></td>";
                                        echo "</tr>";
                                        $itr->next();
                                    }





                                    ?>


                                    <!-- End Generation of table -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

            <!-- Footer -->
            <footer class="sticky-footer bg-white">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>&copy; Hellenic Radio Transient Array 2021</span>
                    </div>
                </div>
            </footer>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Bootstrap core JavaScript-->
    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom scripts for pages-->
    <script src="js/style.min.js"></script>

    <!-- Page level plugins -->
    <script src="vendor/datatables/jquery.datatables.min.js"></script>
    <script src="vendor/datatables/datatables.bootstrap4.min.js"></script>

    <!-- Page level custom scripts -->
    <script src="js/demo/datatables-demo.js"></script>
    <!-- Custom scripts for column toggle-->
    <script type="text/javascript" class="init">
    $('#dataTable').dataTable( {
      "columnDefs": [
        {
            // Hide columns
            "visible": false, "targets": [1,2,6,7,8,11,12,13]
        }
      ]
    } );
    $(document).ready(function() {


    var table = $('#dataTable').DataTable();

    $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();

        // Get the column API object
        var column = table.column( $(this).attr('data-column') );

        // Toggle the visibility
        column.visible( ! column.visible() );
    } );
    } );
    </script>
    <script>
    $(document).ready(function() {
        colorize();
    });
    function colorize() {
        $("tr:even").css("background-color", "#F2F2F2");
        $("tr:odd").css("background-color", "#FFFFFF");
        $("tr:eq(0)").css("background-color", "#ECF3FA");
        //window.setInterval(colorize, 500);
    }
    </script>

</body>

</html>
