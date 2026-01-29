
export function Footer() {
    return (
        <footer className="mt-12 border-t border-slate-200 py-8 text-center text-sm text-slate-500">
            <div className="mx-auto max-w-4xl px-6">
                <p className="mb-4">
                    &copy; {new Date().getFullYear()} Ativo Real. Todos os direitos reservados.
                </p>
                <div className="flex justify-center gap-6">
                    <a href="#" className="hover:text-brand-primary hover:underline">
                        Termos de Uso
                    </a>
                    <a href="#" className="hover:text-brand-primary hover:underline">
                        Política de Privacidade
                    </a>
                    <a href="#" className="hover:text-brand-primary hover:underline">
                        Suporte
                    </a>
                </div>
                <div className="mt-8 rounded-lg bg-blue-50 p-6">
                    <h4 className="font-semibold text-blue-900">Precisa de ajuda profissional?</h4>
                    <p className="mt-2 text-blue-800">
                        Nossa equipe técnica está pronta para auxiliar no cadastramento da sua propriedade.
                    </p>
                    <a
                        href="#"
                        className="mt-4 inline-block rounded-md bg-blue-600 px-6 py-2 font-medium text-white transition-colors hover:bg-blue-700"
                    >
                        Fale com um Especialista
                    </a>
                </div>
            </div>
        </footer>
    )
}
