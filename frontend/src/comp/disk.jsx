function ListItemDisk({ size, loca }) {
  return (
    <small className="mb-0 secotext text-muted">
      <span style={{ fontWeight: "bold" }}>{(size / (1024 * 1024 * 1024)).toFixed(2)} GiB</span> on{" "}
      <span style={{ fontWeight: "bold" }}>{loca}</span>
    </small>
  );
}

export default ListItemDisk;
