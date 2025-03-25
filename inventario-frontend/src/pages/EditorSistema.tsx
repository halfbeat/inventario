import {useParams} from "react-router-dom";
import {useAuth} from "react-oidc-context";
import {useEffect, useRef, useState} from "react";
import {Api, ApiConfig, ListadoPaginadoSistemasDto, RequestParams, SistemaInformacionDto} from "../openapi/api";
import {Configuration} from "../Configuration";
import {Button, Col, Form, Row} from "react-bootstrap";
import {Editor} from '@tinymce/tinymce-react';
import { Editor as TinyMCEEditor } from 'tinymce';

export function EditorSistema() {
    let params = useParams();
    const auth = useAuth();
    const [sistema, setSistema] = useState({} as SistemaInformacionDto);
    const token = auth.user?.access_token;
    const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
    const api = new Api({
        baseUrl: Configuration.backend.baseUrl,
        baseApiParams: rp
    } as ApiConfig);
    const editorRef = useRef<TinyMCEEditor | null>(null);

    useEffect(() => {
        if (params.sistema_id) {
            api.sistemas.getSistemaInformacion(params.sistema_id)
                .then(res => res.data)
                .then(data => {
                    setSistema(data);
                })
                .catch(err => console.error(err));
        }
    }, []);

    return (
        <div>
            <p className={"h5"}>{params.sistema_id}: {sistema?.nombre}</p>
            <hr/>

            <Form>
                <Row className="mb-3">
                    <Form.Group as={Col} md={2} controlId="id">
                        <Form.Label>ID</Form.Label>
                        <Form.Control type="text" placeholder="Id del sistema"/>
                    </Form.Group>
                    <Form.Group as={Col} controlId="nombre">
                        <Form.Label>Nombre</Form.Label>
                        <Form.Control type="text" placeholder="Nombre del sistema"/>
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} md={2} controlId="fecha_registro">
                        <Form.Label>F. Registro</Form.Label>
                        <Form.Control type="date" placeholder="Fecha de registro"/>
                    </Form.Group>
                </Row>
                <Editor
                    licenseKey='test'
                    onInit={(evt, editor) => editorRef.current = editor}
                    initialValue="<p>This is the initial content of the editor.</p>"
                    init={{
                        height: 500,
                        menubar: false,
                        plugins: [
                            'advlist autolink lists link image charmap print preview anchor',
                            'searchreplace visualblocks code fullscreen',
                            'insertdatetime media table paste code help wordcount'
                        ],
                        toolbar: 'undo redo | formatselect | ' +
                            'bold italic backcolor | alignleft aligncenter ' +
                            'alignright alignjustify | bullist numlist outdent indent | ' +
                            'removeformat | help',
                        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
                    }}
                />
                <Button className={"float-end"} variant={"primary"} size={"sm"}>Registrar</Button>
            </Form>
        </div>
    )
}