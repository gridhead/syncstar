function ListItemTask({ mood, loca, time, rate }) {
  return (
    <small className="mb-0 secotext text-muted text-truncate">
      {mood === "PENDING" ? "Waiting for " : ""}
      {mood === "FAILURE" ? "Failed " : ""}
      {mood === "SUCCESS" ? "Completed " : ""}
      {mood === "WORKING" ? "Synchronizing on " : "synchronizing on "}
      <span style={{ fontWeight: "bold" }}>{loca} </span>
      {mood === "WORKING" ? "since " : "after "}
      <span style={{ fontWeight: "bold" }}>{time.toFixed(2)} seconds</span>&nbsp;@&nbsp;
      <span style={{ fontWeight: "bold" }}>{rate}</span>
    </small>
  );
}

export default ListItemTask;
