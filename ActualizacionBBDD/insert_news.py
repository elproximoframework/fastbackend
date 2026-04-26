import os
import json
from sqlalchemy import create_engine, text
from datetime import datetime

# Rutas y URLs de base de datos extraídas de las instrucciones
LOCAL_DB_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_DB_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"
NEWS_DIR = r"D:\YoutubeElProximoFrameworkEnElEspacio\Web\Cloudinary\news"

os.makedirs(NEWS_DIR, exist_ok=True)

# Información de las noticias extraída del guion y los timestamps proporcionados
# YouTube URL de la lista
youtube_link = "https://youtu.be/BRcGwfrXZbA"

news_items = [
    {
        "title": "El misterio del escudo térmico de Artemis II y su reentrada",
        "title_en": "The Mystery of the Artemis II Thermal Shield and its Reentry",
        "excerpt": "Un análisis de las primeras imágenes submarinas del escudo térmico de la cápsula Orion de la misión Artemis II, demostrando su correcto funcionamiento tras una reentrada térmica modificada tipo 'salto'.",
        "excerpt_en": "An analysis of the first underwater images of the Artemis II mission's Orion capsule thermal shield, demonstrating its proper function after a modified 'skip' thermal reentry.",
        "category": "NASA",
        "category_en": "NASA",
        "location": "EEUU",
        "location_en": "USA",
        "date": "2026-04-26",
        "slug": "misterio-escudo-termico-artemis-ii-reentrada",
        "rutanoticia": "260426_artemis_ii.md",
        "tags": ["Artemis", "NASA", "Orion", "Escudo Térmico"],
        "tags_en": ["Artemis", "NASA", "Orion", "Thermal Shield"],
        "timestart": 48,
        "content_es": """# El misterio del escudo térmico de Artemis II y su reentrada

**Fecha:** 2026-04-26

Arrancamos con algo que a los ingenieros de la NASA les estaba quitando el sueño, y no es para menos. Mirad estas imágenes que estáis viendo en pantalla. Parecen sacadas de una película de ciencia ficción submarina, ¿verdad? Pues son fotografías reales tomadas por los buzos de la Marina de los Estados Unidos. Lo que tenéis ahí abajo, sumergido, es la parte inferior de la nave Orion de la misión Artemis II, justo después de su amerizaje el pasado 10 de abril. Y lo más importante de esta imagen no es lo que se ve, sino lo que no se ve: no hay grietas, no falta material de forma catastrófica. El escudo térmico ha aguantado.

Quiero que penséis un poco en lo que significa esto. Esta cápsula venía de regreso a la Tierra a una velocidad de casi 40.000 kilómetros por hora. A esa velocidad, la fricción no es que caliente el aire, es que lo transforma en un plasma abrasador que alcanza la mitad de la temperatura de la superficie del Sol. El escudo térmico de la Artemis II está hecho de un recubrimiento ablativo de fibras de sílice dentro de una resina de polímero. Su trabajo es quemarse y desintegrarse poco a poco para llevarse el calor lejos de los cuatro astronautas que van dentro.

Pero había mucho miedo. Y os cuento por qué. En la misión Artemis I, que no llevaba tripulación, la NASA intentó ser muy innovadora e hizo una reentrada tipo "salto" o "skip reentry". Básicamente, hicieron rebotar la cápsula contra la atmósfera superior de la Tierra, como cuando tiras una piedra plana sobre la superficie de un lago para que dé saltitos. La idea era genial sobre el papel: alargaba la distancia de vuelo antes de caer al Pacífico, mejoraba la precisión y daba un viaje más suave. ¿El problema? Que las pruebas posteriores mostraron que ese rebote permitió que se acumularan bolsas de gas en el material Avcoat del escudo, agrietándolo y haciendo que perdiera trozos enteros, e incluso algunos pernos.

Gente muy respetada, como Charles Camarda, antiguo astronauta e ingeniero de investigación de escudos térmicos tras el desastre del Columbia, llegó a decir que usar ese mismo diseño para la Artemis II era jugar a la ruleta rusa con la vida de los astronautas. Palabras mayores.

Así que la NASA dijo: no vamos a abandonar el salto, pero vamos a hacerlo más pequeño y controlado. Para la Artemis II optaron por una reentrada con un salto modificado, acortando el tiempo que la cápsula pasaba "rebotando" en la atmósfera exterior y haciendo el descenso más pronunciado. Esto evitó la acumulación de presión en el material del escudo térmico. Al hacer esto sacrificaron un poco de distancia de vuelo libre y perdieron parte de la flexibilidad para evitar mal tiempo en la zona de amerizaje, pero fueron a lo seguro para proteger a la tripulación. Y la apuesta les ha salido redonda. Las inspecciones preliminares dicen que la pérdida de material carbonizado fue mínima, las baldosas cerámicas están intactas y la cinta térmica reflectante sigue ahí.

Además, el cohete Space Launch System, el SLS, ese que tanta guerra dio con las fugas y los retrasos, funcionó a la perfección. Y ojo, que la precisión final fue brutal: cayeron a solo 4,7 kilómetros del punto objetivo, con una velocidad de entrada que clavó las predicciones con un margen de error de 1,6 kilómetros por hora. Yo no sé vosotros, pero clavar los números así después de un viaje a la Luna me parece una salvajada técnica. Ahora bien, la NASA dice que todo está "en camino" para el futuro, pero permitidme un poco de escepticismo sano. Artemis III quiere acoplarse con un módulo de aterrizaje lunar en 2027, y Artemis IV y V quieren alunizar en 2028. Sabiendo que los módulos de aterrizaje y los trajes espaciales lunares de nueva generación van con retraso... yo cogería esas fechas con pinzas.
""",
        "content_en": """# The Mystery of the Artemis II Thermal Shield and its Reentry

**Date:** 2026-04-26

We start with something that was keeping NASA engineers awake at night, and for good reason. Look at these images you're seeing on screen. They look like something out of a sci-fi underwater movie, right? Well, they are real photographs taken by US Navy divers. What you have down there, submerged, is the bottom part of the Orion spacecraft from the Artemis II mission, right after its splashdown on April 10. And the most important thing about this image is not what you see, but what you don't see: there are no cracks, there's no catastrophic loss of material. The thermal shield held up.

I want you to think a bit about what this means. This capsule was returning to Earth at a speed of almost 40,000 kilometers per hour. At that speed, friction doesn't just heat the air, it transforms it into scorching plasma that reaches half the temperature of the surface of the Sun. The Artemis II thermal shield is made of an ablative coating of silica fibers within a polymer resin. Its job is to burn away and disintegrate little by little to carry the heat away from the four astronauts inside.

But there was a lot of fear. And I'll tell you why. In the Artemis I mission, which was uncrewed, NASA tried to be very innovative and did a "skip" reentry. Basically, they bounced the capsule off the Earth's upper atmosphere, like skipping a flat stone across a lake. The idea was great on paper: it lengthened the flight distance before falling into the Pacific, improved precision, and provided a smoother ride. The problem? Post-flight tests showed that this bounce allowed gas pockets to accumulate in the Avcoat shield material, cracking it and causing it to lose entire chunks, and even some bolts.

Highly respected people, like Charles Camarda, a former astronaut and thermal shield research engineer after the Columbia disaster, went so far as to say that using that same design for Artemis II was playing Russian roulette with the astronauts' lives. Serious words.

So NASA said: we are not going to abandon the skip, but we are going to make it smaller and controlled. For Artemis II they opted for a modified skip reentry, shortening the time the capsule spent "bouncing" in the outer atmosphere and making the descent steeper. This prevented pressure build-up in the thermal shield material. By doing this they sacrificed a bit of free flight distance and lost some flexibility to avoid bad weather in the splashdown zone, but they played it safe to protect the crew. And their bet paid off perfectly. Preliminary inspections say that the loss of charred material was minimal, the ceramic tiles are intact, and the reflective thermal tape is still there.

In addition, the Space Launch System rocket, the SLS, the one that gave so much trouble with leaks and delays, worked flawlessly. And mind you, the final precision was brutal: they splashed down only 4.7 kilometers from the target point, with an entry speed that nailed the predictions with a margin of error of 1.6 kilometers per hour. I don't know about you, but nailing the numbers like that after a trip to the Moon seems like a technical savage to me. Now, NASA says everything is "on track" for the future, but allow me some healthy skepticism. Artemis III wants to dock with a lunar lander in 2027, and Artemis IV and V want to land on the Moon in 2028. Knowing that the next-generation lunar landers and spacesuits are delayed... I'd take those dates with a grain of salt.
"""
    },
    {
        "title": "Moda orbital: Los trajes a medida y relojes de lujo para la estación espacial de Vast",
        "title_en": "Orbital Fashion: Custom Suits and Luxury Watches for Vast's Space Station",
        "excerpt": "La empresa Vast presenta sus revolucionarios trajes de vuelo a medida y relojes de lujo IWC para los astronautas de su futura estación espacial comercial Haven-1.",
        "excerpt_en": "Vast introduces its revolutionary custom flight suits and luxury IWC watches for the astronauts of its future Haven-1 commercial space station.",
        "category": "Sector Privado",
        "category_en": "Private Sector",
        "location": "EEUU",
        "location_en": "USA",
        "date": "2026-04-26",
        "slug": "moda-orbital-trajes-medida-relojes-lujo-vast",
        "rutanoticia": "260426_vast_trajes.md",
        "tags": ["Vast", "Haven-1", "Trajes Espaciales", "IWC"],
        "tags_en": ["Vast", "Haven-1", "Space Suits", "IWC"],
        "timestart": 260,
        "content_es": """# Moda orbital: Los trajes a medida y relojes de lujo para la estación espacial de Vast

**Fecha:** 2026-04-26

Y hablando de trajes espaciales y de comodidad de los astronautas, vamos a pasar de la supervivencia extrema a la moda orbital. Porque si vas a vivir en el espacio, ¿por qué ir vestido como si fueras a comprar el pan?

La empresa Vast, que está construyendo la que será la primera estación espacial comercial del mundo, la Haven-1, acaba de presentar su traje de vuelo para astronautas. Y mirad qué pasada de diseño. Durante los últimos 25 años, en la Estación Espacial Internacional, los astronautas han usado ropa prácticamente de catálogo. Nos cuenta Drew Feustel, un veterano de la NASA con 225 días en el espacio que ahora lidera a los astronautas en Vast, que el entorno en la ISS se volvió tan seguro que dejaron de usar trajes de vuelo diarios.

Hagamos un poco de historia, que esto es curioso. En la época de Mercury, los astronautas llevaban trajes militares de diferentes ramas, un popurrí tremendo. La famosa foto de los siete de Mercury frente a un caza F-106 hizo que la NASA creara el clásico traje de vuelo azul, más que nada por pura estética fotográfica. En las misiones Mercury y Gemini, las naves eran tan pequeñas que los astronautas no podían ni cambiarse, iban embutidos en los trajes de presión todo el rato. Fue en las misiones Apolo cuando por fin pudieron quitarse las escafandras y estar en mangas de camisa, usando chaquetas y pantalones de fibra de vidrio resistente al fuego. En la estación Skylab usaron un material llamado PBI, que picaba menos. En los transbordadores espaciales llevaban un dos piezas azul lleno de velcro, y a veces hasta pantalones cortos celestes y polos. Pero tras el accidente del Challenger en el 86, volvieron a los trajes de presión para despegues y aterrizajes. ¿Y en la ISS actual? Pues en el segmento estadounidense compran pantalones de senderismo de la marca Cabela's y les cosen trozos de velcro. Literal. Ingeniería aeroespacial de andar por casa.

Pero Vast ha dicho basta. Han diseñado un traje de una o dos piezas, que se puede separar con una cremallera. Está hecho a medida para cada tripulante, tiene aberturas en la espalda y refuerzos en los hombros para mejorar la movilidad en microgravedad, porque allí necesitas moverte en espacios muy reducidos y adoptar posturas raras. Está lleno de bolsillos y velcro para tener las herramientas a mano. Además, es blanco, muy limpio, con parches de la misión y unas "alas" que cada astronauta se gana por vivir y trabajar en órbita.

Y aquí viene el detalle de lujo, la excentricidad de la misión. Cada astronauta de Vast llevará un reloj Pilot's Venturer Vertical Drive, diseñado por la marca suiza IWC Schaffhausen. Lo han rediseñado para el espacio, quitando la corona tradicional y poniendo un bisel giratorio que se puede usar con guantes gruesos. Ha superado pruebas de vibración y cambios de presión. ¿Queréis uno? IWC lo ha puesto a la venta para el público general. Solo cuesta 28.200 dólares. Una ganga, vamos. Si alguno se lo compra, que me deje un comentario.
""",
        "content_en": """# Orbital Fashion: Custom Suits and Luxury Watches for Vast's Space Station

**Date:** 2026-04-26

And speaking of space suits and astronaut comfort, let's move from extreme survival to orbital fashion. Because if you're going to live in space, why dress like you're going to buy bread?

The company Vast, which is building what will be the world's first commercial space station, Haven-1, has just presented its flight suit for astronauts. And look at what an amazing design. Over the past 25 years, on the International Space Station, astronauts have worn virtually off-the-rack clothing. Drew Feustel, a NASA veteran with 225 days in space who now leads astronauts at Vast, tells us that the environment on the ISS became so safe that they stopped wearing daily flight suits.

Let's look at some history, as it's curious. In the Mercury era, astronauts wore military suits from different branches, quite a mix. The famous photo of the Mercury Seven in front of an F-106 fighter jet led NASA to create the classic blue flight suit, mostly for pure photographic aesthetics. On Mercury and Gemini missions, spacecraft were so small astronauts couldn't even change; they were stuffed in pressure suits all the time. It wasn't until the Apollo missions that they could finally take off the helmets and be in shirtsleeves, wearing fire-resistant fiberglass jackets and pants. On the Skylab station, they used a material called PBI, which itched less. On the space shuttles, they wore a blue two-piece full of velcro, and sometimes even light blue shorts and polo shirts. But after the Challenger accident in '86, they went back to pressure suits for takeoffs and landings. And on the current ISS? In the US segment, they buy Cabela's brand hiking pants and sew pieces of velcro onto them. Literally. Homemade aerospace engineering.

But Vast has said enough. They have designed a one or two-piece suit that can be separated with a zipper. It is tailor-made for each crew member, features openings in the back and reinforcements on the shoulders to improve mobility in microgravity, because there you need to move in very tight spaces and adopt weird postures. It is full of pockets and velcro to keep tools handy. Plus, it's white, very clean, with mission patches and "wings" that each astronaut earns for living and working in orbit.

And here comes the luxury detail, the eccentricity of the mission. Each Vast astronaut will wear a Pilot's Venturer Vertical Drive watch, designed by the Swiss brand IWC Schaffhausen. They have redesigned it for space, removing the traditional crown and adding a rotating bezel that can be used with thick gloves. It has passed vibration and pressure change tests. Want one? IWC has put it on sale for the general public. It only costs $28,200. A bargain, really. If anyone buys one, leave me a comment.
"""
    },
    {
        "title": "El telescopio James Webb descubre nubes de hielo en un súper-Júpiter",
        "title_en": "James Webb Telescope Discovers Ice Clouds on a Super-Jupiter",
        "excerpt": "Astrónomos detectan de forma directa con el telescopio espacial James Webb nubes de hielo de agua en Epsilon Indi Ab, un exoplaneta gaseoso gigante a 12 años luz de la Tierra.",
        "excerpt_en": "Astronomers directly detect water ice clouds on Epsilon Indi Ab, a giant gas exoplanet 12 light-years from Earth, using the James Webb Space Telescope.",
        "category": "Ciencia",
        "category_en": "Science",
        "location": "Resto",
        "location_en": "Rest",
        "date": "2026-04-26",
        "slug": "james-webb-nubes-hielo-super-jupiter-epsilon-indi",
        "rutanoticia": "260426_james_webb_epsilon_indi.md",
        "tags": ["James Webb", "Exoplaneta", "Epsilon Indi", "Astronomía"],
        "tags_en": ["James Webb", "Exoplanet", "Epsilon Indi", "Astronomy"],
        "timestart": 464,
        "content_es": """# El telescopio James Webb descubre nubes de hielo en un súper-Júpiter

**Fecha:** 2026-04-26

Siguiendo con nuestro repaso, vamos a alejarnos un poco de la Tierra. Concretamente a 12 años luz, en la constelación austral de Indus. Allí está la estrella Epsilon Indi A, una enana naranja un poco más pequeña y fría que nuestro Sol, que tiene entre 3.700 y 5.700 millones de años. Pues bien, el telescopio espacial James Webb ha vuelto a hacer magia.

Los astrónomos han usado el instrumento MIRI (el instrumento de infrarrojo medio) del Webb para tomar imágenes directas de un exoplaneta gigante gaseoso que orbita esa estrella, llamado Epsilon Indi Ab. Este bicho es lo que llamamos un súper-Júpiter. Tiene 7,6 veces la masa de nuestro Júpiter, aunque su diámetro es más o menos el mismo. Fijaos en la densidad que debe tener eso.

Lo fascinante es lo que han encontrado en su atmósfera. La temperatura en este planeta es de entre 200 y 300 Kelvin, es decir, entre 70 grados bajo cero y 20 grados Celsius positivos. Es un poco más cálido que nuestro Júpiter, que está a unos gélidos 133 grados bajo cero, y esto se debe a que Epsilon Indi Ab todavía conserva calor de su fase de formación. Con el paso de miles de millones de años, se irá enfriando.

Los científicos, liderados por un estudiante de doctorado del Instituto Max Planck llamado Bhavesh Rajpoot, esperaban encontrar enormes cantidades de gas amoníaco en la atmósfera, porque en nuestro Júpiter el amoníaco domina las capas superiores. Sin embargo, al analizar los datos fotométricos del Webb, vieron que había mucho menos amoníaco del esperado. ¿La explicación? El planeta está cubierto por nubes gruesas pero irregulares de hielo de agua, muy parecidas a las nubes cirros de gran altitud que tenemos aquí en la Tierra.

Es increíble. Estamos hablando de que el James Webb no solo detecta un planeta a 12 años luz, sino que nos dice el parte meteorológico: "cielos parcialmente nubosos con nubes de hielo de agua, y menos olor a amoníaco de lo previsto". Como dice el doctor James Mang de la Universidad de Texas, esto antes parecía imposible y ahora estamos sondeando la estructura tridimensional de atmósferas alienígenas. Es un triunfo absoluto de la ingeniería óptica.
""",
        "content_en": """# James Webb Telescope Discovers Ice Clouds on a Super-Jupiter

**Date:** 2026-04-26

Continuing with our review, let's move a bit further away from Earth. Specifically to 12 light-years away, in the southern constellation of Indus. There lies the star Epsilon Indi A, an orange dwarf slightly smaller and cooler than our Sun, which is between 3.7 and 5.7 billion years old. Well, the James Webb Space Telescope has worked its magic again.

Astronomers have used Webb's MIRI instrument (Mid-Infrared Instrument) to take direct images of a giant gas exoplanet orbiting that star, named Epsilon Indi Ab. This beast is what we call a super-Jupiter. It has 7.6 times the mass of our Jupiter, although its diameter is roughly the same. Imagine the density it must have.

What's fascinating is what they've found in its atmosphere. The surface temperature on this planet is between 200 and 300 Kelvin, meaning between minus 70 degrees Celsius and plus 20 degrees Celsius. It's a bit warmer than our Jupiter, which stands at a frigid minus 133 degrees Celsius, and this is because Epsilon Indi Ab still retains heat from its formation phase. Over billions of years, it will continue to cool down.

The scientists, led by a PhD student from the Max Planck Institute named Bhavesh Rajpoot, expected to find huge amounts of ammonia gas in the atmosphere, because on our Jupiter, ammonia dominates the upper layers. However, when analyzing the Webb's photometric data, they saw there was much less ammonia than expected. The explanation? The planet is covered by thick but patchy clouds of water ice, very similar to the high-altitude cirrus clouds we have here on Earth.

It's incredible. We are talking about the James Webb not only detecting a planet 12 light-years away but giving us the weather report: "partly cloudy skies with water ice clouds, and less smell of ammonia than expected." As Dr. James Mang of the University of Texas says, this previously seemed impossible and now we are probing the three-dimensional structure of alien atmospheres. It is an absolute triumph of optical engineering.
"""
    },
    {
        "title": "Ingeniería de origami en los nuevos satélites lanzados por Rocket Lab",
        "title_en": "Origami Engineering in New Satellites Launched by Rocket Lab",
        "excerpt": "Rocket Lab completa su lanzamiento número 79 poniendo en órbita satélites de la agencia japonesa JAXA, incluyendo uno con una asombrosa antena desplegable de diseño origami.",
        "excerpt_en": "Rocket Lab completes its 79th launch, placing satellites for the Japanese agency JAXA into orbit, including one with an amazing origami-design deployable antenna.",
        "category": "Sector Privado",
        "category_en": "Private Sector",
        "location": "Resto",
        "location_en": "Rest", # New Zealand / Japan
        "date": "2026-04-26",
        "slug": "rocket-lab-lanzamiento-satelites-jaxa-origami",
        "rutanoticia": "260426_rocket_lab_origami.md",
        "tags": ["Rocket Lab", "Electron", "JAXA", "Origami"],
        "tags_en": ["Rocket Lab", "Electron", "JAXA", "Origami"],
        "timestart": 585,
        "content_es": """# Ingeniería de origami en los nuevos satélites lanzados por Rocket Lab

**Fecha:** 2026-04-26

Y volviendo a nuestro vecindario orbital, hablemos de lanzamientos y satélites, porque el tráfico espacial está imposible.

Por un lado, la empresa Rocket Lab, desde su base en Nueva Zelanda, lanzó el pasado miércoles 22 de abril su cohete Electron en la misión bautizada como "Kakushin Rising". Este es el lanzamiento número 79 de este pequeño pero matón cohete de 18 metros de altura. Han puesto en órbita baja terrestre, a unos 540 kilómetros de altura, ocho satélites japoneses para la agencia JAXA.

Es la segunda misión de este tipo que hacen para Japón, la anterior fue en diciembre. Pero lo curioso de esta carga útil es la variedad. Han subido pequeños satélites educativos, uno de monitorización oceánica, cámaras multiespectrales ultrapequeñas... y mi favorito: un satélite con una antena desplegable basada en técnicas de origami. Literalmente, han doblado la antena como si fuera una grulla de papel para que ocupe lo mínimo en el cohete, y una vez en el espacio, se despliega hasta alcanzar 25 veces su tamaño original. Me imagino a los ingenieros japoneses doblando la antena con un cuidado milimétrico, es una genialidad. Por cierto, Rocket Lab también usa una versión modificada de este cohete, llamada HASTE, para vuelos suborbitales donde prueban tecnologías hipersónicas. Esta gente no para.
""",
        "content_en": """# Origami Engineering in New Satellites Launched by Rocket Lab

**Date:** 2026-04-26

And returning to our orbital neighborhood, let's talk about launches and satellites, because space traffic is impossible.

On one hand, the company Rocket Lab, from its base in New Zealand, launched its Electron rocket last Wednesday, April 22, in the mission dubbed "Kakushin Rising." This is the 79th launch of this small but mighty 18-meter-tall rocket. They have placed eight Japanese satellites for the JAXA agency into low Earth orbit, at about 540 kilometers altitude.

This is the second mission of this type they've done for Japan, the previous one was in December. But the curious thing about this payload is the variety. They have sent up small educational satellites, an ocean monitoring one, ultra-small multispectral cameras... and my favorite: a satellite with a deployable antenna based on origami techniques. Literally, they folded the antenna like a paper crane so it takes up minimal space on the rocket, and once in space, it deploys to reach 25 times its original size. I imagine Japanese engineers folding the antenna with millimeter-level care, it's genius. By the way, Rocket Lab also uses a modified version of this rocket, called HASTE, for suborbital flights where they test hypersonic technologies. These people don't stop.
"""
    },
    {
        "title": "Misión SMILE: La alianza entre Europa y China para estudiar el viento solar",
        "title_en": "SMILE Mission: Europe and China Team Up to Study Solar Wind",
        "excerpt": "La misión conjunta SMILE se prepara para su lanzamiento en 2026 desde la Guayana Francesa a bordo del Vega-C, con el objetivo de observar la interacción de la Tierra con el clima espacial.",
        "excerpt_en": "The joint SMILE mission prepares for launch in 2026 from French Guiana aboard a Vega-C, aiming to observe Earth's interaction with space weather.",
        "category": "Agencias",
        "category_en": "Agencies",
        "location": "Europa",
        "location_en": "Europe",
        "date": "2026-04-26",
        "slug": "mision-smile-alianza-europa-china-viento-solar",
        "rutanoticia": "260426_mision_smile.md",
        "tags": ["ESA", "CNSA", "SMILE", "Viento Solar"],
        "tags_en": ["ESA", "CNSA", "SMILE", "Solar Wind"],
        "timestart": 678,
        "content_es": """# Misión SMILE: La alianza entre Europa y China para estudiar el viento solar

**Fecha:** 2026-04-26

Por otro lado, apuntad esta fecha: 19 de mayo de 2026. Ese día, desde el Puerto Espacial Europeo en la Guayana Francesa, la Agencia Espacial Europea (la ESA) y la Academia China de Ciencias van a lanzar la misión SMILE. El lanzamiento se pospuso un poco por un problema técnico en la línea de producción de un componente del cohete europeo Vega-C, pero ya está todo solucionado y el satélite está encerrado en la cofia, listo para volar.

¿Qué va a hacer SMILE? Pues va a ser nuestro meteorólogo del clima espacial. Su objetivo es ver cómo responde la Tierra a los flujos de partículas y ráfagas de radiación que nos escupe el Sol. Lleva una cámara de rayos X para observar el campo magnético de la Tierra, y una cámara ultravioleta que va a grabar las auroras boreales sin interrupción durante 45 horas seguidas. El vuelo va a ser tenso: las cuatro etapas del cohete Vega-C se irán separando, liberarán a SMILE en órbita baja a los 57 minutos, y a los 63 minutos desplegará sus paneles solares. A partir de ahí, la propia nave se propulsará hasta una órbita con forma de huevo, alejándose hasta 121.000 kilómetros sobre el Polo Norte para recoger datos, y bajando hasta 5.000 kilómetros sobre el Polo Sur para enviar esos datos a las estaciones terrestres. Una coreografía orbital perfecta.
""",
        "content_en": """# SMILE Mission: Europe and China Team Up to Study Solar Wind

**Date:** 2026-04-26

On the other hand, note this date: May 19, 2026. On that day, from Europe's Spaceport in French Guiana, the European Space Agency (ESA) and the Chinese Academy of Sciences will launch the SMILE mission. The launch was slightly postponed due to a technical problem on the production line of an element of the European Vega-C rocket, but everything is now solved, and the satellite is safely enclosed in the fairing, ready to fly.

What will SMILE do? Well, it will be our space weather meteorologist. Its goal is to see how Earth responds to the particle flows and radiation bursts the Sun spits at us. It carries an X-ray imager to observe the Earth's magnetic field, and an ultraviolet imager that will record the auroras continuously for 45 hours. The flight will be tense: the Vega-C rocket's four stages will separate, releasing SMILE into low orbit at 57 minutes, and at 63 minutes it will deploy its solar panels. From there, the spacecraft itself will propel into an egg-shaped orbit, moving out to 121,000 kilometers over the North Pole to collect data, and dipping to 5,000 kilometers over the South Pole to send that data to ground stations. A perfect orbital choreography.
"""
    },
    {
        "title": "SpaceX y Falcon Heavy listos para lanzar el gigantesco satélite ViaSat-3 F3",
        "title_en": "SpaceX and Falcon Heavy Ready to Launch Massive ViaSat-3 F3 Satellite",
        "excerpt": "Un cohete Falcon Heavy pondrá en órbita en 2026 el satélite ViaSat-3 F3, capaz de proporcionar internet de banda ancha de más de 1 Terabit por segundo a la región de Asia-Pacífico.",
        "excerpt_en": "A Falcon Heavy rocket will place the ViaSat-3 F3 satellite into orbit in 2026, capable of providing broadband internet over 1 Terabit per second to the Asia-Pacific region.",
        "category": "SpaceX",
        "category_en": "SpaceX",
        "location": "EEUU",
        "location_en": "USA",
        "date": "2026-04-26",
        "slug": "spacex-falcon-heavy-viasat-3-internet-terabit",
        "rutanoticia": "260426_viasat3_falcon_heavy.md",
        "tags": ["SpaceX", "Falcon Heavy", "ViaSat-3", "Telecomunicaciones"],
        "tags_en": ["SpaceX", "Falcon Heavy", "ViaSat-3", "Telecommunications"],
        "timestart": 757,
        "content_es": """# SpaceX y Falcon Heavy listos para lanzar el gigantesco satélite ViaSat-3 F3

**Fecha:** 2026-04-26

Y si hablamos de coreografías pesadas, tenemos que hablar de SpaceX y Viasat. El lunes 27 de abril de 2026, desde el mítico Complejo de Lanzamiento 39A del Centro Espacial Kennedy, un imponente Falcon Heavy de SpaceX va a poner en órbita el satélite ViaSat-3 F3.

Este monstruo ha sido construido por Boeing Satellite Systems y es el tercer y último satélite de la constelación global de banda Ka de ultra-alta capacidad de Viasat. Su misión: dar internet de banda ancha a toda la región de Asia-Pacífico. Y cuando digo banda ancha, me refiero a que este bicho puede proporcionar más de 1 Terabit por segundo de rendimiento de red. 1 Tbps desde el espacio. Con esto, Viasat completa su red global, uniéndose a los satélites que ya cubren las Américas y la región EMEA (Europa, Medio Oriente y África). El Falcon Heavy lo dejará en una órbita de transferencia, y luego el satélite usará su propia propulsión eléctrica durante meses para llegar a su órbita geoestacionaria final. Entrará en servicio a finales del verano de 2026, tras probar el complejísimo despliegue de sus reflectores y su radiador.
""",
        "content_en": """# SpaceX and Falcon Heavy Ready to Launch Massive ViaSat-3 F3 Satellite

**Date:** 2026-04-26

And if we're dealing with heavy choreographies, we must talk about SpaceX and Viasat. On Monday, April 27, 2026, from the legendary Launch Complex 39A at the Kennedy Space Center, an imposing SpaceX Falcon Heavy rocket will put the ViaSat-3 F3 satellite into orbit.

This monster was built by Boeing Satellite Systems and is the third and final satellite in Viasat's global ultra-high-capacity Ka-band constellation. Its mission: to provide broadband internet to the entire Asia-Pacific region. And when I say broadband, I mean this beast can deliver over 1 Terabit per second of network throughput. 1 Tbps from space. With this, Viasat completes its global network, joining satellites already covering the Americas and the EMEA region (Europe, Middle East, and Africa). The Falcon Heavy will drop it in a transfer orbit, and then the satellite will use its own electric propulsion over months to reach its final geostationary orbit. It will enter service in late summer 2026, after testing the highly complex deployment of its reflectors and radiator.
"""
    },
    {
        "title": "El inmenso plan espacial de China: Centros de datos en órbita y diplomacia en expansión",
        "title_en": "China's Massive Space Plan: Orbital Data Centers and Expanding Diplomacy",
        "excerpt": "China anuncia una ambiciosa agenda para 2026 que incluye propuestas multimillonarias para enviar centros de datos al espacio y misiones conjuntas con el 'Sur Global' como Brasil y Pakistán.",
        "excerpt_en": "China announces an ambitious 2026 agenda featuring multibillion-dollar proposals for space data centers and joint missions with the 'Global South,' such as Brazil and Pakistan.",
        "category": "Agencias",
        "category_en": "Agencies",
        "location": "China",
        "location_en": "China",
        "date": "2026-04-26",
        "slug": "plan-espacial-china-2026-centros-de-datos-orbita",
        "rutanoticia": "260426_china_data_center.md",
        "tags": ["CNSA", "China", "Diplomacia Espacial", "Centros de Datos"],
        "tags_en": ["CNSA", "China", "Space Diplomacy", "Data Centers"],
        "timestart": 824,
        "content_es": """# El inmenso plan espacial de China: Centros de datos en órbita y diplomacia en expansión

**Fecha:** 2026-04-26

Pero esperad, que si hablamos de Asia, tenemos que hablar del gigante asiático. China ha pisado el acelerador y se le ha roto el freno.

Primero, una noticia financiera que parece ciencia ficción: una startup espacial con sede en Beijing acaba de conseguir 8.400 millones de dólares en compromisos de financiación de bancos vinculados al estado chino. ¿Para qué? Para construir centros de datos en órbita para el año 2035. Sí, servidores en el espacio. Según el CEO de la empresa estadounidense Voyager Technologies, que también está en esta carrera junto a SpaceX o Google, poner centros de datos en órbita solucionaría los problemas insaciables de energía que tienen en la Tierra, evitaría las quejas de los vecinos que no quieren una nave industrial ruidosa al lado de su casa, y esquivaría muchas trabas regulatorias. Básicamente, si la inteligencia artificial requiere una energía brutal para procesar datos, China quiere poner los servidores en el espacio y alimentarlos con energía solar ininterrumpida. Es un plan ambicioso y con 8.400 millones de respaldo, van muy en serio.

Y esto es solo la punta del iceberg del programa espacial chino. La Administración Nacional del Espacio de China (la CNSA) acaba de dar una rueda de prensa espectacular para anunciar sus planes de 2026, coincidiendo con el 11º Día del Espacio de China y el 70 aniversario de su industria espacial.

Para que os hagáis una idea del ritmo que llevan: en 2025 realizaron 92 misiones de lanzamiento. ¡92! Eso es un 35% más que en 2024. Su cohete Larga Marcha-2D ya ha logrado 100 lanzamientos exitosos consecutivos. Y no se quedan en lo tradicional; ya han hecho vuelos inaugurales de sus cohetes reutilizables Zhuque-3 y Larga Marcha-12A. Sí, la competencia para los Falcon de SpaceX ya está aquí.

Para 2026, la agenda es una locura. Van a lanzar la misión tripulada Shenzhou-23. Van a hacer pruebas de vuelo de múltiples cohetes reutilizables. Y en exploración profunda, la sonda Tianwen-2 se acercará al asteroide 2016HO3 para realizar observaciones cercanas y una futura toma de muestras. Además, siguen liberando terabytes de datos científicos de su misión marciana Tianwen-1 para que científicos de todo el mundo puedan usarlos.

Pero lo que me parece más estratégico de los planes de China es su diplomacia espacial. El experto Kang Guohua comentaba que el programa chino, a diferencia de los occidentales que tienden a cooperar entre países desarrollados, está extendiendo sus alas hacia el "Sur Global". Por ejemplo, van a continuar su histórico programa de Satélites de Recursos Terrestres con Brasil (el programa CBERS), que lleva funcionando desde 1988 y cuyos datos ayudan a toda América Latina, África y Asia.

Y el broche de oro de esta diplomacia: el Primer Ministro de Pakistán, Shehbaz Sharif, acaba de reunirse con Zeeshan Ali y Khurram Daud. ¿Quiénes son? Pues los dos candidatos pakistaníes que han sido seleccionados para el programa espacial tripulado de China. Van a entrenar para viajar a la estación espacial china, Tiangong. El Primer Ministro estaba exultante, diciendo que es un orgullo nacional y que la amistad entre Pakistán y China está "lista para alcanzar las estrellas". Es un movimiento geopolítico brillante por parte de China, ofreciendo acceso al espacio a naciones que no tienen infraestructura propia.
""",
        "content_en": """# China's Massive Space Plan: Orbital Data Centers and Expanding Diplomacy

**Date:** 2026-04-26

But wait, if we are talking about Asia, we have to talk about the Asian giant. China has stepped on the gas and broken the brake pedal.

First, financial news that sounds like science fiction: a Beijing-based space startup just secured $8.4 billion in funding commitments from state-linked banks. For what? To build orbital data centers by 2035. Yes, servers in space. According to the CEO of American firm Voyager Technologies, which is also in this race alongside SpaceX or Google, putting data centers in orbit would solve the insatiable energy problems they have on Earth, avoid complaints from neighbors who don't want a noisy industrial warehouse next door, and skirt many regulatory hurdles. Basically, if artificial intelligence requires massive energy to process data, China wants to put the servers in space and power them with continuous solar energy. It's an ambitious plan, and with 8.4 billion backing it, they are dead serious.

And this is just the tip of the iceberg for the Chinese space program. The China National Space Administration (CNSA) just held a spectacular press conference to announce its 2026 plans, coinciding with the 11th Space Day of China and the 70th anniversary of its space industry.

To give you an idea of their pace: in 2025 they performed 92 launch missions. 92! That is 35% more than in 2024. Its Long March-2D rocket has already achieved 100 consecutive successful launches. And they don't stick only to tradition; they have already made maiden flights of their reusable Zhuque-3 and Long March-12A rockets. Yes, the competition for SpaceX Falcons is already here.

For 2026, the agenda is crazy. They will launch the crewed Shenzhou-23 mission. They will run flight tests of multiple reusable rockets. And in deep space exploration, the Tianwen-2 probe will approach asteroid 2016HO3 for close observations and a future sample return. Also, they continue to release terabytes of scientific data from their Martian Tianwen-1 mission so scientists worldwide can use it.

But what seems most strategic about China's plans is its space diplomacy. Expert Kang Guohua noted that the Chinese program, unlike Western ones which tend to cooperate among developed nations, is spreading its wings toward the "Global South." For example, they will continue their historic Earth Resources Satellite program with Brazil (the CBERS program), which has been operating since 1988 and whose data aids all of Latin America, Africa, and Asia.

And the crowning jewel of this diplomacy: the Prime Minister of Pakistan, Shehbaz Sharif, just met with Zeeshan Ali and Khurram Daud. Who are they? They are the two Pakistani candidates selected for China's crewed space program. They will train to travel to the Chinese space station, Tiangong. The Prime Minister was ecstatic, stating it's a national pride and that the friendship between Pakistan and China is "ready to reach the stars." It's a brilliant geopolitical move by China, offering space access to nations lacking their own infrastructure.
"""
    }
]

def create_markdown_files():
    for item in news_items:
        # File path for Spanish
        es_path = os.path.join(NEWS_DIR, item['rutanoticia'])
        # File path for English (insert _en before .md)
        base, ext = os.path.splitext(item['rutanoticia'])
        en_path = os.path.join(NEWS_DIR, f"{base}_en{ext}")
        
        with open(es_path, "w", encoding="utf-8") as f:
            f.write(item['content_es'])
            
        with open(en_path, "w", encoding="utf-8") as f:
            f.write(item['content_en'])
            
def insert_into_db(db_url):
    engine = create_engine(db_url)
    try:
        with engine.begin() as conn:
            for item in news_items:
                # Format tags as JSON
                tags_json = json.dumps(item['tags'])
                tags_en_json = json.dumps(item['tags_en'])
                
                # Check if it already exists slightly to avoid duplicates if possible
                query_check = text("SELECT id FROM news WHERE slug = :slug")
                res = conn.execute(query_check, {"slug": item['slug']}).fetchone()
                
                if res is None:
                    insert_query = text("""
                        INSERT INTO news (
                            title, title_en, excerpt, excerpt_en, category, category_en, 
                            location, location_en, covered, date, slug, tags, tags_en, 
                            featured, linkyoutube, rutanoticia, timestart, show
                        ) VALUES (
                            :title, :title_en, :excerpt, :excerpt_en, :category, :category_en,
                            :location, :location_en, false, :date, :slug, :tags, :tags_en,
                            true, :linkyoutube, :rutanoticia, :timestart, true
                        )
                    """)
                    conn.execute(insert_query, {
                        "title": item['title'],
                        "title_en": item['title_en'],
                        "excerpt": item['excerpt'],
                        "excerpt_en": item['excerpt_en'],
                        "category": item['category'],
                        "category_en": item['category_en'],
                        "location": item['location'],
                        "location_en": item['location_en'],
                        "date": item['date'],
                        "slug": item['slug'],
                        "tags": tags_json,
                        "tags_en": tags_en_json,
                        "linkyoutube": youtube_link,
                        "rutanoticia": item['rutanoticia'],
                        "timestart": item['timestart']
                    })
                    print(f"[{db_url}] Inserted: {item['title']}")
                else:
                    print(f"[{db_url}] Skipped (already exists): {item['title']}")
    except Exception as e:
        print(f"[{db_url}] Error during DB operation: {e}")

if __name__ == "__main__":
    print("Creando archivos Markdown...")
    create_markdown_files()
    print("Archivos Markdown creados.")
    
    print("\nInsertando en base local...")
    insert_into_db(LOCAL_DB_URL)
    
    print("\nInsertando en base remota (Railway)...")
    insert_into_db(REMOTE_DB_URL)
    print("\nProceso terminado.")
