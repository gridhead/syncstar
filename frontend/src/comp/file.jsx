function ListItemFile({ size, suit }) {
  return (
    <small className="mb-0 secotext text-muted">
      Requires at least{" "}
      <span style={{ fontWeight: "bold" }} className={`${suit}`}>
        {(size / (1024 * 1024 * 1024)).toFixed(2)} GiB
      </span>{" "}
      of storage
    </small>
  );
}

export default ListItemFile;
