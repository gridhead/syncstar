import { Container, Navbar } from "react-bootstrap";

import packInfo from "../../package.json";

function MainNavbar() {
  return (
    <Navbar className="navbar navbar-expand-lg fixed-top" bg="body-secondary" data-bs-theme="light">
      <Container>
        <Navbar.Brand href="#" className="headelem text-success">
          SyncStar
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>v{packInfo.version}</Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default MainNavbar;
