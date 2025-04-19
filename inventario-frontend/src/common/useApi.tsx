import React, {useEffect} from "react";
import {Api, ApiConfig, RequestParams} from "../openapi/api";
import {useAuth} from "react-oidc-context";

export default function useApi() {
    const auth = useAuth();
    const token = auth.user?.access_token;

    const [api, setApi] = React.useState<Api<any>>();

    useEffect(() => {
        const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
        const api = new Api({
            baseUrl: window.REACT_APP_BACKEND_BASE_URL,
            baseApiParams: rp
        } as ApiConfig);

        setApi(api);
    }, [token]);

    return api;
}