import { Container, Navbar } from "react-bootstrap";

function MainNavbar() {
  const versdata = "0.1.0";
  return (
    <Navbar className="bg-success navbar navbar-expand-lg fixed-top navbar-dark">
      <Container>
        <Navbar.Brand href="#home" className="headelem">
          SyncStar
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>v{versdata}</Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default MainNavbar;
