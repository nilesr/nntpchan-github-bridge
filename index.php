<?php
$payload = json_decode($_POST["payload"], true);
foreach ($payload["commits"] as $commit) {
	$fd = fopen("/tmp/payload", "w");
	fwrite($fd, "New commit to " . $payload["repository"]["full_name"]);
	fwrite($fd, "\n");
	fwrite($fd, "\t" . $commit["message"]);
	fwrite($fd, "\n");
	fwrite($fd, "\t");
	if (count($commit["modified"]) > 0) {
		fwrite($fd, "Modified: " . implode(", ", $commit["modified"]));
	}
	if (count($commit["added"]) > 0) {
		fwrite($fd, "; Added: " . implode(", ", $commit["added"]));
	}
	if (count($commit["removed"]) > 0) {
		fwrite($fd, "; Removed: " . implode(", ", $commit["removed"]));
	}
	fwrite($fd, "\n");
	fwrite($fd, "\t" . $commit["timestamp"] . " " . $commit["id"]);
	fwrite($fd, "\n");
	fwrite($fd, "\t" . $commit["url"]);
	fclose($fd);
	exec("python3 /opt/post.py /tmp/payload");
}
?>
