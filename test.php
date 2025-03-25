<?php 

add_action('wp_head','custom_head_page');
function custom_head_page(){
    ?>

    <style>
		.home-play-form {
		margin-top: 30px;
	}
    .jackpot-value-container img {
        max-width: 300px;
    }

    .jackpot-value-container {
		position: relative;
		top: -100px;
		margin-bottom: -100px;
		
	}
	.jackpot-value-container img {
		max-width: 300px;
		mix-blend-mode: unset;
	}
	.jackpot-value-container + .text img {
		max-width: 85%;
	}
    .jackpot-value-container .value {
        color: white;
        position: absolute;
        left: 50%;
        transform: translate(-50%,-50%);
        top: 49%;
        font-size: 25px;
        font-weight: bolder;
		width: 100%;
    }

    @media screen and (max-width:566px){
        .jackpot-value-container img {
            max-width: 100%;
        }
        .jackpot-value-container .value {
            font-size: 21px;
        }
    }
    </style>
    <?php
}
get_header(); ?>

<!-- main content -->
<div class="main-content">

	<?php if (get_field('home_introduction','option')): ?>
	<section class="section section-home-intro section-padding">
		<h1 class="d-none"><?php echo get_the_title(); ?></h1>
		<div class="container">
		<div class="row">
			
			<?php if (get_field('sliders')): ?>
			<div class="col-12 col-md-12 col-lg-6 my-auto">
				
				<div class="swiper swiper-home-intro">
					<div class="swiper-wrapper">
						
						<?php foreach (get_field('sliders') as $slider): ?>
						<div class="swiper-slide">
							<div class="banner-container">
								<div class="main">
									<img 
										 alt="<?php echo get_field( 'casino_name','option' ); ?> Slide" 
										 title="<?php echo get_field( 'casino_name','option' ); ?> Slide" 
										 src="<?php echo $slider['main_image']; ?>" class="img-fluid"/>
								</div>
								<div class="jackpot-value-container image-placeholder text-center">
									<img 
										 alt="<?php echo get_field( 'casino_name','option' ); ?> Bonus" 
										 title="<?php echo get_field( 'casino_name','option' ); ?> Bonus" 
										 src="<?php echo $slider['placeholder']; ?>" class="img-fluid"/>
									<div class="value">
										<span class="currency-code"></span>
										<span class="count counter" data-count="1900320"></span>
									</div>
								</div>
								<div class="text text-center mt-3 mb-3 mb-md-0">
									<img 
										 alt="<?php echo get_field( 'casino_name','option' ); ?> Text" 
										 title="<?php echo get_field( 'casino_name','option' ); ?> Text" 
										 src="<?php echo $slider['text']; ?>" class="img-fluid"/>
								</div>
							</div>
						</div>
						<?php endforeach; ?>
					</div>
				</div>
				
				
			</div>
			<?php endif; ?>
			<div class="col-12 col-md-12 col-lg-6 my-auto">
				
				<div class="home-play-form">
					
					<div class="row">
						<div class="col-md-6">
							<div class="py-0">
								<div class="text-center">
									<img 
										 alt="<?php echo get_field( 'casino_name','option' ); ?> Promo" 
										 title="<?php echo get_field( 'casino_name','option' ); ?> Promo"
										 src="<?php echo get_field('home_introduction','option')['promotional_image']; ?>" class="img-fluid"/>
								</div>

								<div class="action mt-2">
									<a class="btn btn-generic"
									   href="<?php echo home_url(); ?>/promotions/">READ MORE</a>
								</div>
							</div>
						</div>
						<div class="col-md-6 my-auto">
							<form class="generic-play-form p-3">
								<div class="form-group">
									<input name="name" class="form-control" placeholder="Your Name"/>
								</div>
								<div class="form-group">
									<input type="email" name="email" class="form-control" placeholder="Your Email"/>
								</div>
								
								<div class="form-group">
									<input name="your-currency" class="currency-code-value form-control" placeholder="Currency" readonly/>
								</div>
								
								<label class="acceptance" for="acceptance">
									<input checked id="acceptance" type="checkbox" name="your-acceptance"/>I accepted the terms and conditions & privacy policy.
								</label>

								<div class="action">
									<button type="button" class="btn btn-generic-2">SIGN UP</button>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>

		
		</div>
		
	
	</section>

	
	<?php endif ;?>


	
	<?php
	$games_id = get_page_by_title( 'Games' );
	$childrens = get_children($games_id->ID,);
	$slots_id = get_page_by_title( 'Slots' );
	$slots_id = $slots_id->ID;

	?>
  <section class="section section-generic-background section-games">
      

		<div class="game-types-container">
			<div class="container">
				<div class="row">
					<div class="col-md-12 col-lg-12">
						<ul class="game-types">

						<li data-id="<?php echo $slots_id; ?>" class="active"><?php echo get_the_title($slots_id); ?></li>
								
							<?php 
							$count = 1;
							foreach ($childrens as $children): 
								if ($children->ID == $slots_id) continue;
								if (get_post_type($children) <> 'page') continue;
								
								?>
							<li 
								data-id="<?php echo $children->ID; ?>">
								<a href="<?php echo get_the_permalink($children->ID); ?>">
									<?php echo $children->post_title; ?>
								</a>
								</li>
							<?php 
								$count++;
							endforeach; ?>
						</ul>
					</div>
				</div>
			</div>
		</div>

		<div class="slot-games-container p-5">
			<div class="container">

				<div class="text-center mb-4">
					<h2>SLOTS</h2>
					<?php the_ai_data('slots_description'); ?>
				</div>
				<?php 
			
				$args = array(
					'post_parent' => $slots_id,
					'post_type'   => 'page', // Specify post type if needed, e.g., 'post', 'page', etc.
					'post_status' => 'publish', // Specify post status if needed, e.g., 'publish', 'draft', etc.
					'posts_per_page' => -1,    // To retrieve all children
					'orderby'     => 'title', // Order by menu order or any other field
					'order'       => 'ASC', // Order direction, can be 'ASC' or 'DESC',
					'meta_query'  => array(
						array(
							'key'     => '_wp_page_template',
							'value'   => 'page-templates/page-slot.php', // Specify the page template file name
							'compare' => '=', // Comparison operator, use '=' for exact match
						),
					)
				);

				$query = new WP_Query($args);
				$first_post = null;
				if ($query->have_posts()) {
					
				?>
				<div class="row">
					<?php 
					
					while ($query->have_posts()) {
						$query->the_post();
						
						if (!$first_post) {
							$first_post = get_the_ID();
						}
					?>
						<div class="col-6 col-sm-6 col-md-6 col-lg-3">
							<div class="slot-item mb-4 text-center">

								<div class="image">
									<a href="<?php echo get_the_permalink(); ?>">
										<?php if (get_field('image')): ?>
                                            <img src="<?php echo get_field('image'); ?>"
											 alt="<?php echo get_the_title(); ?>" 
											 title="<?php echo get_the_title(); ?>" 
											 class="img-fluid">
                                        <?php endif; ?>
									</a>
								</div>
								<h3><?php echo get_the_title(); ?></h3>

								<div class="action">
									<div class="row">
										<div class="col-md-6 col-lg-6">
											<a class="btn-generic" href="#play" data-redirect="<?php echo get_the_ID(); ?>">PLAY NOW</a>
										</div>
										<div class="col-md-6 col-lg-6">
											<a class="btn-generic-2" href="<?php echo get_the_permalink(); ?>">READ REVIEW</a>
										</div>
									</div>
								</div>
							</div>
						</div>
					<?php 
					 	}
						wp_reset_postdata();
					}
					
					?>
					
				</div>
			</div>
		</div>

  </section>
	
	<section class="section section-generic-content section-padding">
		<div class="container">
			<div class="intro-content mt-3">
				
				<article class="article">
				<?php the_ai_data('main_content'); ?>
				
				<?php the_ai_data('promotion'); ?>
				</article>
				
			</div>
		</div>
	</section>
  


</div>

<?php get_footer(); ?>
