% rebase('layout', title='Registrar')

<section class="form-section">
    <div class="form-card">

        <h1 class="form-title">Registrar</h1>

        <form action="/users/register" method="post">

            <div class="input-group">
                <input type="text" id="name" name="name" required placeholder="Nome"
                       value="{{ name or '' }}">
            </div>

            <div class="input-group">
                <input type="email" id="email" name="email" required placeholder="Email"
                       value="{{ email or '' }}">
            </div>

            <div class="input-group">
                <input type="password" id="password" name="password" required placeholder="Senha">
            </div>

            <div class="btn-group">
                <button type="submit" class="btn btn-primary">Registrar</button>
                <a href="/login" class="btn btn-secondary">Voltar</a>
            </div>

        </form>
    </div>
</section>
