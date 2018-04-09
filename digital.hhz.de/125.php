<?php
	// Variable declaration - Entity IDs for sensors
	$entIdTemp = "sensor.125_temp_a"; // Temperature
	$entIdHum = "sensor.125_hum_a"; // Humidity
	$entIdMot = "sensor.125_motion_a"; // Motion
	$entIdAir = "sensor.125_co2_a"; // Air Quality
	$entIdLight = "sensor.125_light_a"; // Light
	
	// Variable declaration - Room name
	$valRoom = "EG-125";
	
	// Obtain sensor values
	include("sensorvalues.inc.php");
?>


<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<link rel="stylesheet" href="_css/styles.css">
		<title>Digital HHZ - EG-125 sensor values</title>
		
		<!-- Import jQuery libraries for the card flip effect -->
		<script src="_js/jquery-3.2.1.min.js"></script>
		
		<script>
			function flip(panelName) {
				$(panelName).toggleClass('flipped');
			}
		</script>
	</head>
	
	<body>
	
		<!-- Include the header bar -->
		<?php include("header.standard.inc.php"); ?>
		
		<div class="wrapper">
		
			<!-- Temperature -->
			<div class="container">
				<div class="tile" id="tileTemp" onclick=flip('#tileTemp')>
					<!-- Front face -->
					<div class="front temperature">
						<div class="heading" id="headingTemp">Temperatur in °C</div>
						<br>
						<div class="value" id ="valueTemp"> <?php echo $valTemp ?> </div>
						<br>
						<div class="showdetails" id="showdetailsTemp"> Details anzeigen </div>					
					</div>
					
					<!-- Back face -->
					<div class="back temperature">
							<div class="heading">Details</div>
							<div class="detailHeading">Sensortyp</div>
							<div class="detailValue"><?php echo $valTypeTemp ?></div>
							<div class="detailHeading">Zuletzt aktualisiert</div>
							<div class="detailValue"><?php echo $valUpdatedTemp ?></div>
							<div class="detailHeading">Durchschnittswert pro Stunde</div>
							<div class="detailValue"><?php echo $valAverageTemp . "°C" ?></div>
					</div>
				</div>
			</div>
			
			
			<!-- Humidity -->
			<div class="container">
				<div class="tile" id="tileHum" onclick=flip('#tileHum')>
					<!-- Front face -->
					<div class="front humidity">
						<div class="heading">Luftfeuchtigkeit in %</div>
						<br>
						<div class="value"> <?php echo $valHum ?> </div>
						<br>
						<div class="showdetails"> Details anzeigen </div>				
					</div>
					
					<!-- Back face -->
					<div class="back humidity">
						<div class="heading">Details</div>
						<div class="detailHeading">Sensortyp</div>
						<div class="detailValue"><?php echo $valTypeHum ?></div>
						<div class="detailHeading">Zuletzt aktualisiert</div>
						<div class="detailValue"><?php echo $valUpdatedHum ?></div>
						<div class="detailHeading">Durchschnittswert pro Stunde</div>
						<div class="detailValue"><?php echo $valAverageHum . "%" ?></div>
					</div>
				</div>
			</div>
		

			<!-- Air Quality -->
			<div class="container">
				<div class="tile" id="tileAir" onclick=flip('#tileAir')>
					<!-- Front face -->
					<div class="front airquality">
						<div class="heading">Luftqualität in ppm</div>
						<br>
						<div class="value"> <?php echo $valAir ?> </div>
						<br>
						<div class="showdetails"> Details anzeigen </div>					
					</div>
					
					<!-- Back face -->
					<div class="back airquality">
						<div class="heading">Details</div>
						<div class="detailHeading">Sensortyp</div>
						<div class="detailValue"><?php echo $valTypeAir ?></div>
						<div class="detailHeading">Zuletzt aktualisiert</div>
						<div class="detailValue"><?php echo $valUpdatedAir ?></div>
						<div class="detailHeading">Durchschnittswert pro Stunde</div>
						<div class="detailValue"><?php echo $valAverageAir . "ppm" ?></div>
					</div>
				</div>
			</div>


			<!-- Light -->
			<div class="container">
				<div class="tile" id="tileLight" onclick=flip('#tileLight')>
					<!-- Front face -->
					<div class="front light">
						<div class="heading">Helligkeit in lx</div>
						<br>
						<div class="value"> <?php echo $valLight ?> </div>
						<br>
						<div class="showdetails"> Details anzeigen </div>
					</div>
					
					<!-- Back face -->
					<div class="back light">
						<div class="heading">Details</div>
						<div class="detailHeading">Sensortyp</div>
						<div class="detailValue"><?php echo $valTypeLight ?></div>
						<div class="detailHeading">Zuletzt aktualisiert</div>
						<div class="detailValue"><?php echo $valUpdatedLight ?></div>
						<div class="detailHeading">Durchschnittswert pro Stunde</div>
						<div class="detailValue"><?php echo $valAverageLight . "lx" ?></div>
					</div>
				</div>
			</div>
		</div>
		
	</body>

</html>
