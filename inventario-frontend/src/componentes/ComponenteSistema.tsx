import {Card, Col, Form, Row} from "react-bootstrap";
import {Editor} from "@tinymce/tinymce-react";
import React, {useEffect, useRef, useState} from "react";
import {ComponenteSistemaDto} from "../openapi/api";
import {Editor as TinyMCEEditor} from "tinymce";
import {SubmitHandler, useForm} from "react-hook-form";
import useApi from "../common/useApi";

interface ComponenteSistemaProps {
    sistemaId?: string | null
    componenteId?: string | null
}

type FormProps = {
    nombre: string,
    gitUrl: string | undefined,
    observaciones: string | undefined,
}

export const ComponenteSistema = ({sistemaId, componenteId}: ComponenteSistemaProps) => {
    const api = useApi();
    const [componente, setComponente] = useState<ComponenteSistemaDto | null>(null);
    const editorRef = useRef<TinyMCEEditor | null>(null);
    const {
        register,
        handleSubmit,
        setValue,
        // formState: {errors},
    } = useForm<FormProps>()

    useEffect(() => {
        if (sistemaId && componenteId && api) {
            api.sistemas.getComponenteSistemaInformacion(sistemaId, componenteId)
                .then(res => res.data)
                .then(data => {
                    setComponente(data);
                    setValue('nombre', data.nombre);
                    setValue("gitUrl", data.git_repo)
                    setValue("observaciones", data.observaciones)
                    editorRef.current?.setContent(data.observaciones || '')
                })
                .catch(err => console.error(err));
        }
    }, [sistemaId, componenteId, api]);

    const onSubmit: SubmitHandler<FormProps> = (data) => {
        data.observaciones = editorRef.current?.getContent()
        const componenteDtp = {
            nombre: data.nombre,
            observaciones: data.observaciones
        } as ComponenteSistemaDto;
        if (api) {

        }
    }

    return (
        <Card >
            <Card.Header><b>{componente?.nombre || 'NUEVO COMPONENTE'}</b></Card.Header>
            <Card.Body>
                <Form onSubmit={handleSubmit(onSubmit)}>
                    <Row className="mb-3">
                        <Form.Group as={Col} controlId="nombre">
                            <Form.Label>Nombre</Form.Label>
                            <Form.Control type="text" placeholder="Nombre del componente" {...register("nombre")}/>
                        </Form.Group>
                    </Row>
                    <Row className="mb-3">
                        <Form.Group as={Col} controlId="git-url">
                            <Form.Label>Repositorio Git</Form.Label>
                            <Form.Control type="text"
                                          placeholder="Dirección http del repositorio Git" {...register("gitUrl")}/>
                        </Form.Group>
                    </Row>
                    <Row className="mb-3">
                        <Form.Group as={Col} md={12} controlId="observaciones">
                            <Form.Label>Observaciones</Form.Label>

                            <Editor
                                tinymceScriptSrc={`${process.env.PUBLIC_URL}/tinymce/tinymce.min.js`}
                                onInit={(evt, editor) => editorRef.current = editor}
                                initialValue={componente?.observaciones}
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
                </Form>
            </Card.Body>
        </Card>
    )
}