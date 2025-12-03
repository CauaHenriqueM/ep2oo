% rebase('layout', title='Login')

<section class="form-section">
    <div class="form-card">

        <h1 class="form-title">Login</h1>

        <form action="/login" method="post">

            <div class="input-group">
                <input type="email" id="email" name="email" required placeholder="Email"
                       value="{{ email or '' }}">
            </div>

            <div class="input-group">
                <input type="password" id="password" name="password" required placeholder="Senha">
            </div>

            <div class="btn-group">
                <button type="submit" class="btn btn-primary">Entrar</button>

                <a href="/users/register" class="btn btn-secondary">Cadastrar</a>
            </div>

        </form>
    </div>
</section>
