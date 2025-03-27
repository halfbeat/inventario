import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {Home} from "../pages/Home";
import {SessionExpired} from "../pages/SessionExpired";
import ListadoSistemas from "../pages/ListadoSistemas";
import EditorSistema from "../pages/EditorSistema";
import RegistroSistema from "../pages/RegistroSistema";

export function Layout() {
    return (
        <Container className="Template-container">
            <Header></Header>
            <div className="Template-content ">
                <Routes>
                    <Route index element={<Home/>}/>
                    <Route path={"/home"} element={<Home/>}/>
                    <Route path={"/session-expired"} element={<SessionExpired/>}/>
                    <Route path={"/sistemas"} element={<ListadoSistemas/>}/>
                    <Route path={"/sistemas/registro"} element={<RegistroSistema/>}/>
                    <Route path={"/sistemas/:sistema_id"} element={<EditorSistema/>}/>
                </Routes>
            </div>
            <Footer></Footer>
        </Container>
    );
}