function ListItemTask({ mood, loca, time, rcrd }) {
  return (
    <small className="mb-0 secotext text-muted">
      {mood === "PENDING" ? "Waiting for " : ""}
      {mood === "FAILURE" ? "Failed " : ""}
      {mood === "SUCCESS" ? "Completed " : ""}
      {mood === "WORKING" ? "Synchronizing on " : "synchronizing on "}
      <span style={{ fontWeight: "bold" }}>{loca} </span>
      {mood === "WORKING" ? "since " : "after "}
      <span style={{ fontWeight: "bold" }}>{time.toFixed(2)} seconds </span>({rcrd} records written)
    </small>
  );
}

export default ListItemTask;
