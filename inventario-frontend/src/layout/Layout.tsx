import {Container} from "react-bootstrap";
import {Header} from "./Header";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Footer} from "./Footer";
import {Home} from "../pages/Home";
import {ListadoSistemas} from "../pages/ListadoSistemas";
import {EditorSistema} from "../pages/EditorSistema";
import {RegistroSistema} from "../pages/RegistroSistema";
import {ProtectedRoute} from "../ProtectedRoute";

export function Layout() {
    return (
        <BrowserRouter basename={process.env.PUBLIC_URL}>
            <Container className="Template-container p-0 ">
                <Header></Header>
                <div className="Template-content p-2 m-0">
                    <Routes>
                        <Route index element={<Home/>}/>
                        <Route path={"/home"} element={<Home/>}/>
                        <Route path={"/"} element={<ProtectedRoute/>}>
                            <Route path={"/sistemas"} element={<ListadoSistemas/>}/>
                            <Route path={"/sistemas/registro"} element={<RegistroSistema/>}/>
                            <Route path={"/sistemas/:sistema_id"} element={<EditorSistema/>}/>
                        </Route>
                    </Routes>
                </div>
                <Footer></Footer>
            </Container>
        </BrowserRouter>

    );
}