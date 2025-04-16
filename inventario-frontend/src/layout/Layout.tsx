import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {Home} from "../pages/Home";
import {SessionExpired} from "../pages/SessionExpired";
import ListadoSistemasPAge from "../pages/ListadoSistemas";
import EditorSistemaPage from "../pages/EditorSistema";
import RegistroSistemaPage from "../pages/RegistroSistema";
import QueryDir3Page from "../pages/QueryDir3";
import ComponentesSistemaPage from "../pages/ComponentesSistemaPage";

export function Layout() {
    return (
        <Container className="Template-container">
            <Header></Header>
            <div className="Template-content ">
                <Routes>
                    <Route index element={<Home/>}/>
                    <Route path={"/home"} element={<Home/>}/>
                    <Route path={"/session-expired"} element={<SessionExpired/>}/>
                    <Route path={"/dir3"} element={<QueryDir3Page codigo_unidad={"A07009156"} label={"Código unidad"}/>}/>
                    <Route path={"/sistemas"} element={<ListadoSistemasPAge/>}/>
                    <Route path={"/sistemas/registro"} element={<RegistroSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id"} element={<EditorSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id/componentes"} element={<ComponentesSistemaPage/>}/>
                </Routes>
            </div>
            <Footer></Footer>
        </Container>
    );
}