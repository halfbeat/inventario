
import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {HomePage} from "../pages/HomePage";
import {SessionExpiredPage} from "../pages/SessionExpiredPage";
import ListadoSistemasPAge from "../pages/BuscadorSistemasPage";
import EditorSistemaPage from "../pages/EditorSistemaPage";
import RegistroSistemaPage from "../pages/RegistroSistemaPage";
import ComponentesSistemaPage from "../pages/ComponentesSistemaPage";
import QueryDir3 from "../componentes/QueryDir3";
import NuevoComponenteSistemaPage from "../pages/NuevoComponenteSistemaPage";
import EdicionComponenteSistemaPage from "../pages/EdicionComponenteSistemaPage";

export function Layout() {
    return (
        <Container className="Template-container">
            <Header></Header>
            <div className="Template-content ">
                <Routes>
                    <Route index element={<HomePage/>}/>
                    <Route path={"/home"} element={<HomePage/>}/>
                    <Route path={"/session-expired"} element={<SessionExpiredPage/>}/>
                    <Route path={"/dir3"} element={<QueryDir3 codigo_unidad={"A07009156"} label={"Código unidad"}/>}/>
                    <Route path={"/sistemas"} element={<ListadoSistemasPAge/>}/>
                    <Route path={"/sistemas/registro"} element={<RegistroSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id"} element={<EditorSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id/componentes"} element={<ComponentesSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id/componentes/registro"} element={<NuevoComponenteSistemaPage/>}/>
                    <Route path={"/sistemas/:sistema_id/componentes/:componente_id"} element={<EdicionComponenteSistemaPage/>}/>
                </Routes>
            </div>
            <Footer></Footer>
        </Container>
    );
}