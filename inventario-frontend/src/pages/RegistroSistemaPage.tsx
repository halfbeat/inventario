import {useAuth, withAuthenticationRequired} from "react-oidc-context";
import React, {useRef, useState} from "react";
import {Button, Col, Form, Row} from "react-bootstrap";
import {Editor} from "@tinymce/tinymce-react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Api, ApiConfig, RequestParams, SistemaInformacionDto} from "../openapi/api";
import {Editor as TinyMCEEditor} from "tinymce";
import {SubmitHandler, useForm} from "react-hook-form";
import {useNavigate} from "react-router-dom";
import QueryDir3 from "../componentes/QueryDir3";
import useApi from "../common/useApi";

const RegistroSistemaPage = () => {
    const auth = useAuth();
    const token = auth.user?.access_token;
    const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
    const api = useApi();

    const editorRef = useRef<TinyMCEEditor | null>(null);
    const [sistema, setSistema] = useState({} as SistemaInformacionDto);
    const [unidadResponsableFuncional, setUnidadResponsableFuncional] = useState<string | undefined>('');

    type FormProps = {
        id: string
        nombre: string,
        observaciones: string | undefined,
    }
    const {
        register,
        handleSubmit,
        setValue,
        // formState: {errors},
    } = useForm<FormProps>()

    const navigate = useNavigate()

    function handleOnChange(codigoDir3: string | undefined): void {
        setUnidadResponsableFuncional(codigoDir3)
    }

    const onSubmit: SubmitHandler<FormProps> = (data) => {
        data.observaciones = editorRef.current?.getContent()
        const sistemaDto = {
            sistema_id: data.id,
            nombre: data.nombre,
            unidad_responsable: unidadResponsableFuncional,
            observaciones: data.observaciones
        } as SistemaInformacionDto;
        if (api) {
            api.sistemas.registrarSistemaInformacion(sistemaDto)
                .then(res => res.data)
                .then(data => {
                    setSistema(data);
                    setValue('id', data.sistema_id)
                    setValue('nombre', data.nombre)
                    setValue('observaciones', data.observaciones)
                    setUnidadResponsableFuncional(data.unidad_responsable)
                    navigate(`/sistemas/${data.sistema_id}`)
                })
                .catch(err => alert(JSON.stringify(err)));
        }
    }

    return (
        <div>
            <p className={"h4 border border-2 rounded p-2"}>Registro de un nuevo sistema</p>

            <Form onSubmit={handleSubmit(onSubmit)}>
                <Row className="mb-3">
                    <Form.Group as={Col} md={2} controlId="id">
                        <Form.Label>ID</Form.Label>
                        <Form.Control type="text" placeholder="Id del sistema" {...register("id")}/>
                    </Form.Group>
                    <Form.Group as={Col} controlId="nombre">
                        <Form.Label>Nombre</Form.Label>
                        <Form.Control type="text" placeholder="Nombre del sistema" {...register("nombre")}/>
                    </Form.Group>
                </Row>
                <Row>
                    <QueryDir3 codigo_unidad={unidadResponsableFuncional} label={"Unidad responsable"}
                               onChange={handleOnChange}/>
                </Row>
                {/*<Row className="mb-3">*/}
                {/*    <Form.Group as={Col} md={2} controlId="fecha_registro">*/}
                {/*        <Form.Label>F. Registro</Form.Label>*/}
                {/*        <Form.Control type="date" placeholder="Fecha de registro"/>*/}
                {/*    </Form.Group>*/}
                {/*</Row>*/}
                <Row className="mb-3">
                    <Form.Group as={Col} md={12} controlId="observaciones">
                        <Form.Label>Observaciones</Form.Label>

                        <Editor
                            tinymceScriptSrc={`${process.env.PUBLIC_URL}/tinymce/tinymce.min.js`}
                            onInit={(evt, editor) => editorRef.current = editor}
                            initialValue={sistema.observaciones}
                            init={{
                                height: 300,
                                menubar: false,
                                plugins: [
                                    // 'advlist autolink lists link image charmap print preview anchor',
                                    // 'searchreplace visualblocks code fullscreen',
                                    // 'insertdatetime media table paste code help wordcount'
                                ],
                                toolbar: 'undo redo | formatselect | ' +
                                    'bold italic backcolor | alignleft aligncenter ' +
                                    'alignright alignjustify | bullist numlist outdent indent | ' +
                                    'removeformat | help',
                                content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
                            }}
                        />
                    </Form.Group>
                </Row>
                <div className={"text-end mt-3"}>
                    <Button type={"submit"} className={" "} variant={"primary"}>
                        <FontAwesomeIcon icon={"floppy-disk"}/> Registrar
                    </Button>
                </div>
            </Form>
        </div>
    )
}

export default withAuthenticationRequired(RegistroSistemaPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});