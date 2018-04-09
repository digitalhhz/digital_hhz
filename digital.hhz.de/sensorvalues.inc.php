<?php
	// Variable declaration - Obtain credentials for MySQL
	include(PATH TO CREDENTIALS);	
	
	// Variable declaration - Details
	$valTypeTemp = "DHT-11";
	$valTypeHum = "DHT-11";
	$valTypeAir = "REHAU Ambient Air";
	$valTypeLight = "BH-1750";
	$valTypeDoor = "STM-250";
	$valTypeWindow1 = "STM-250";
	$valTypeWindow2 = "STM-250";
	$valUpdatedTemp = "";
	$valUpdatedHum = "";
	$valUpdatedAir = "";
	$valUpdatedLight = "";
	$valUpdateFrequency = "Every 60  minutes";

	// Variable declaration - Sensor values
	$valTemp = ""; // Temperature
	$valHum = ""; // Humidity
	$valMot = ""; // Motion
	$valAir = ""; // Air Quality
	$valLight = ""; // Light
			
	$valAverageTemp = "";
	$valAverageHum = "";
	$valAverageAir = "";
	$valAverageLight = "";

	// Connect to MYsQL database
	try {
		$myDB = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
		// set the PDO error mode to exception
		$myDB->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);	
		
		// ################# //
		// Get sensor values //
		// ################# //
		
		// Query and extract temperature value
		$resTemp = $myDB->query("SELECT state FROM states WHERE entity_id = '" . $entIdTemp . "' ORDER BY created DESC LIMIT 1");
		foreach($resTemp as $row) {
			$valTemp = $row['state'];
		}
		
		// Query and extract humidity value

		$resHum = $myDB->query("SELECT state FROM states WHERE entity_id = '" . $entIdHum . "' ORDER BY created DESC LIMIT 1");
		foreach($resHum as $row) {
			$valHum = $row['state'];
		}	
		
		// Query and extract motion value
		$resMot = $myDB->query("SELECT state FROM states WHERE entity_id = '" . $entIdMot . "' ORDER BY created DESC LIMIT 1");
		foreach($resMot as $row) {
			$valMot = $row['state'];
		}
		
		// Query and extract air quality value
		$resAir = $myDB->query("SELECT state FROM states WHERE entity_id = '" . $entIdAir . "' ORDER BY created DESC LIMIT 1");
		foreach($resAir as $row) {
			$valAir = $row['state'];
		}
		
		// Query and extract light value
		$resLight = $myDB->query("SELECT state FROM states WHERE entity_id = '" . $entIdLight . "' ORDER BY created DESC LIMIT 1");
		foreach($resLight as $row) {
			$valLight = $row['state'];
		}
		
		
		// ########################################## //
		// Get the timestamp of the last value update //
		// ########################################## //
		
		// Query and extract timestamp for temperature
		$resTemp = $myDB->query("SELECT created FROM states WHERE entity_id = '" . $entIdTemp . "' ORDER BY created DESC LIMIT 1");
		foreach($resTemp as $row) {
			$valUpdatedTemp = $row['created'];
		}
		
		// Query and extract timestamp for humidity
		$resHum = $myDB->query("SELECT created FROM states WHERE entity_id = '" . $entIdHum . "' ORDER BY created DESC LIMIT 1");
		foreach($resHum as $row) {
			$valUpdatedHum = $row['created'];
		}	
		
		// Query and extract timestamp for air quality
		$resAir = $myDB->query("SELECT created FROM states WHERE entity_id = '" . $entIdAir . "' ORDER BY created DESC LIMIT 1");
		foreach($resAir as $row) {
			$valUpdatedAir = $row['created'];
		}	
		
		// Query and extract timestamp for light
		$resLight = $myDB->query("SELECT created FROM states WHERE entity_id = '" . $entIdLight . "' ORDER BY created DESC LIMIT 1");
		foreach($resLight as $row) {
			$valUpdatedLight = $row['created'];
		}	
		
		

		// ####################################### //
		// Get the average sensor value over 1 day //
		// ####################################### //
		
		// Query and extract timestamp for temperature
		$resTemp = $myDB->query("SELECT ROUND(AVG(state),2) AS avg FROM states WHERE entity_id = '" . $entIdTemp . "' ORDER BY created DESC");
		foreach($resTemp as $row) {
			$valAverageTemp = $row['avg'];
		}
		
		// Query and extract timestamp for humidity
		$resHum = $myDB->query("SELECT ROUND(AVG(state),2) AS avg FROM states WHERE entity_id = '" . $entIdHum . "' ORDER BY created DESC");
		foreach($resHum as $row) {
			$valAverageHum = $row['avg'];
		}	
		
		// Query and extract timestamp for air quality
		$resAir = $myDB->query("SELECT ROUND(AVG(state),2) AS avg FROM states WHERE entity_id = '" . $entIdAir . "' ORDER BY created DESC");
		foreach($resAir as $row) {
			$valAverageAir = $row['avg'];
		}	
		
		// Query and extract timestamp for light
		$resLight = $myDB->query("SELECT ROUND(AVG(state),2) AS avg FROM states WHERE entity_id = '" . $entIdLight . "' ORDER BY created DESC");
		foreach($resLight as $row) {
			$valAverageLight = $row['avg'];
		}
	
	
	
	} catch(PDOException $e){
		echo "Connection to database failed. Sensor values could not be obtained.";
	}
?>
