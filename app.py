from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, TextAreaField, DateField, BooleanField, HiddenField, SubmitField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_migrate import Migrate
from models import db, Project, Raam
import os
from datetime import datetime
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jouw-geheime-sleutel-hier')

# Database configuratie
database_url = os.environ.get('DATABASE_URL', 'sqlite:///gordijn_meting.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Maak de uploads map aan in dezelfde directory als de database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Zorg ervoor dat de uploads map bestaat
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProjectForm(FlaskForm):
    projectnummer = StringField('Projectnummer', validators=[DataRequired()])
    klant = StringField('Klant', validators=[DataRequired()])
    locatie = StringField('Locatie', validators=[DataRequired()])
    datum = DateField('Datum', validators=[DataRequired()])
    opmerkingen = TextAreaField('Project Opmerkingen')

class RaamForm(FlaskForm):
    project_id = HiddenField()
    ruimte = StringField('Ruimte', validators=[DataRequired()])
    raamtype = SelectField('Raamtype', choices=[
        ('standaard', 'Standaard'),
        ('schuifpui', 'Schuifpui'),
        ('frans balkon', 'Frans Balkon'),
        ('andere', 'Andere')
    ])
    breedte = FloatField('Breedte (cm)', validators=[DataRequired()])
    hoogte = FloatField('Hoogte (cm)', validators=[DataRequired()])
    plafondhoogte = FloatField('Plafondhoogte (cm)', validators=[DataRequired()])
    ophangsysteem = SelectField('Ophangsysteem', choices=[
        ('rail', 'Rail'),
        ('stang', 'Stang'),
        ('andere', 'Andere')
    ])
    montagewijze = SelectField('Montagewijze', choices=[
        ('plafond', 'Plafond'),
        ('wand', 'Wand'),
        ('andere', 'Andere')
    ])
    rail_lengte = FloatField('Rail lengte (cm)', validators=[DataRequired()])
    stof = StringField('Stof')
    voering = SelectField('Voering', choices=[
        ('geen', 'Geen'),
        ('standaard', 'Standaard'),
        ('thermisch', 'Thermisch'),
        ('andere', 'Andere')
    ])
    plooi = SelectField('Plooi', choices=[
        ('geen', 'Geen'),
        ('standaard', 'Standaard'),
        ('andere', 'Andere')
    ])
    motorisatie = BooleanField('Motorisatie')
    opmerkingen = TextAreaField('Opmerkingen')
    foto = FileField('Foto')
    submit = SubmitField('Opslaan')

@app.route('/')
def index():
    logger.debug('Index route accessed')
    try:
        projecten = Project.query.all()
        return render_template('index.html', projecten=projecten)
    except Exception as e:
        logger.error(f'Error in index route: {str(e)}')
        return str(e), 500

@app.route('/project/nieuw', methods=['GET', 'POST'])
def nieuw_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            projectnummer=form.projectnummer.data,
            klant=form.klant.data,
            locatie=form.locatie.data,
            datum=form.datum.data,
            opmerkingen=form.opmerkingen.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project succesvol aangemaakt!', 'success')
        return redirect(url_for('project_details', project_id=project.id))
    
    return render_template('nieuw_project.html', form=form)

@app.route('/project/<int:project_id>')
def project_details(project_id):
    project = Project.query.get_or_404(project_id)
    ramen = Raam.query.filter_by(project_id=project_id).all()
    return render_template('project_details.html', project=project, ramen=ramen)

@app.route('/project/<int:project_id>/nieuw_raam', methods=['GET', 'POST'])
def nieuw_raam(project_id):
    project = Project.query.get_or_404(project_id)
    form = RaamForm()
    form.project_id.data = project_id

    if form.validate_on_submit():
        raam = Raam(
            project_id=project_id,
            ruimte=form.ruimte.data,
            raamtype=form.raamtype.data,
            breedte=form.breedte.data,
            hoogte=form.hoogte.data,
            plafondhoogte=form.plafondhoogte.data,
            ophangsysteem=form.ophangsysteem.data,
            montagewijze=form.montagewijze.data,
            rail_lengte=form.rail_lengte.data,
            stof=form.stof.data,
            voering=form.voering.data,
            plooi=form.plooi.data,
            motorisatie=form.motorisatie.data,
            opmerkingen=form.opmerkingen.data
        )

        if form.foto.data:
            file = form.foto.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                raam.foto = filename

        db.session.add(raam)
        db.session.commit()
        flash('Raam succesvol toegevoegd!', 'success')
        return redirect(url_for('project_details', project_id=project_id))
    
    return render_template('nieuw_raam.html', form=form, project=project)

@app.route('/project/<int:project_id>/raam/<int:raam_id>/bewerk', methods=['GET', 'POST'])
def bewerk_raam(project_id, raam_id):
    project = Project.query.get_or_404(project_id)
    raam = Raam.query.get_or_404(raam_id)
    
    if raam.project_id != project_id:
        flash('Dit raam behoort niet tot het geselecteerde project.', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    form = RaamForm()
    form.project_id.data = project_id

    if form.validate_on_submit():
        raam.ruimte = form.ruimte.data
        raam.raamtype = form.raamtype.data
        raam.breedte = form.breedte.data
        raam.hoogte = form.hoogte.data
        raam.plafondhoogte = form.plafondhoogte.data
        raam.ophangsysteem = form.ophangsysteem.data
        raam.montagewijze = form.montagewijze.data
        raam.rail_lengte = form.rail_lengte.data
        raam.stof = form.stof.data
        raam.voering = form.voering.data
        raam.plooi = form.plooi.data
        raam.motorisatie = form.motorisatie.data
        raam.opmerkingen = form.opmerkingen.data

        if form.foto.data:
            file = form.foto.data
            if file and allowed_file(file.filename):
                # Verwijder oude foto als die er is
                if raam.foto:
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], raam.foto))
                    except:
                        pass
                
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                raam.foto = filename

        db.session.commit()
        flash('Raam succesvol bijgewerkt!', 'success')
        return redirect(url_for('project_details', project_id=project_id))
    
    # Vul het formulier met bestaande gegevens
    form.ruimte.data = raam.ruimte
    form.raamtype.data = raam.raamtype
    form.breedte.data = raam.breedte
    form.hoogte.data = raam.hoogte
    form.plafondhoogte.data = raam.plafondhoogte
    form.ophangsysteem.data = raam.ophangsysteem
    form.montagewijze.data = raam.montagewijze
    form.rail_lengte.data = raam.rail_lengte
    form.stof.data = raam.stof
    form.voering.data = raam.voering
    form.plooi.data = raam.plooi
    form.motorisatie.data = raam.motorisatie
    form.opmerkingen.data = raam.opmerkingen
    
    return render_template('bewerk_raam.html', form=form, project=project, raam=raam)

@app.route('/project/<int:project_id>/bewerk', methods=['GET', 'POST'])
def bewerk_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    
    if form.validate_on_submit():
        project.projectnummer = form.projectnummer.data
        project.klant = form.klant.data
        project.locatie = form.locatie.data
        project.datum = form.datum.data
        project.opmerkingen = form.opmerkingen.data
        
        db.session.commit()
        flash('Project succesvol bijgewerkt!', 'success')
        return redirect(url_for('project_details', project_id=project.id))
    
    # Vul het formulier met bestaande gegevens
    form.projectnummer.data = project.projectnummer
    form.klant.data = project.klant
    form.locatie.data = project.locatie
    form.datum.data = project.datum
    form.opmerkingen.data = project.opmerkingen
    
    return render_template('bewerk_project.html', form=form, project=project)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    logger.debug('Starting application')
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5001, debug=True)
else:
    # Dit zorgt ervoor dat de database wordt aangemaakt wanneer de app op Render draait
    with app.app_context():
        db.create_all() 